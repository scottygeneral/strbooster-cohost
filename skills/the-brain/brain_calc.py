#!/usr/bin/env python3
"""The Brain calculator (STR Booster playbook, step 1).

Reads brain-data.json (the answers from the interview), works out NOI,
cap rate, break-even and calibrated targets for each property and the
portfolio, and writes the numbers section of business-brain.md.

Usage:
    python brain_calc.py brain-data.json --md business-brain.md [--json results.json]

Standard library only. All money is annual unless a field says otherwise.
"""
import argparse
import json
import sys

# Rough rules of thumb, as a share of total revenue. Used only to flag lines
# worth a second look, never as facts about a market.
BENCHMARKS = {
    "management": (0.15, 0.30, "Full-service managers usually charge 15% to 30%."),
    "platform": (0.03, 0.16, "Platform fees usually run 3% to 16%, depending on the fee setting."),
    "utilities": (0.04, 0.10, "Utilities and internet usually run 4% to 10%."),
    "repairs": (0.02, 0.05, "Repairs and maintenance usually run 2% to 5%."),
    "reserve": (0.02, 0.05, "A replacement reserve of 2% to 5% covers furniture, linens and appliances."),
}
NOI_MARGIN_FLOOR = 0.25  # below this, small shocks erase the year
OCC_CEILING = 0.85  # few STRs hold more than this all year

UTILITY_KEYS = {"electric", "water", "gas", "internet", "trash", "sewer", "utilities", "cable"}
REPAIR_KEYS = {"repairs", "repairs_maintenance", "maintenance"}

PLAYBOOK = {
    4: "Step 4, Optimize Your Listings",
    5: "Step 5, OTA Distribution",
    6: "Step 6, Marketing And Sales",
    7: "Step 7, Revenue Management",
    8: "Step 8, Scale Up: Win More Homes",
    9: "Step 9, Guest Experience",
}


def money(x):
    if x is None:
        return "n/a"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct(x, digits=1):
    if x is None:
        return "n/a"
    return f"{x * 100:.{digits}f}%"


def label(val, est):
    return f"{val} (Est.)" if est else val


def property_model(p, levers=None):
    """Return the numbers for one property, optionally after lever moves."""
    rev = p["revenue"]
    costs = p.get("costs", {})
    booked = rev["booked_nights"]
    available = rev["available_nights"]
    rent = rev["rent"]
    cleaning_fees = rev.get("cleaning_fees", 0.0)
    other = rev.get("other_income", 0.0)
    stays = rev.get("stays") or (booked / rev["avg_stay_nights"])

    adr = rent / booked
    los = booked / stays
    # cleaning fees and other income scale with stays and nights
    cleaning_fee_per_stay = cleaning_fees / stays
    other_per_night = other / booked

    pct_costs = dict(costs.get("percent_of_revenue", {}))
    per_stay = dict(costs.get("per_stay", {}))
    fixed = dict(costs.get("fixed_annual", {}))
    reserve_pct = p.get("reserve_pct", 0.03)

    if levers:
        booked = min(available * levers["occ_cap"], booked + available * levers["occ_pts"] / 100.0)
        booked = max(booked, rev["booked_nights"])
        adr = adr * (1 + levers["adr_pct"] / 100.0)
        if levers.get("adr_cap"):
            adr = max(rev["rent"] / rev["booked_nights"], min(adr, levers["adr_cap"]))
        stays = booked / los
        cut = levers.get("cost_cut_pct", 0) / 100.0
        per_stay = {k: v * (1 - cut) for k, v in per_stay.items()}
        fixed = {k: v * (1 - cut) for k, v in fixed.items()}

    rent = adr * booked
    cleaning_fees = cleaning_fee_per_stay * stays
    other = other_per_night * booked
    total_rev = rent + cleaning_fees + other

    lines = []
    for k, r in pct_costs.items():
        lines.append(("variable", k, r * total_rev))
    lines.append(("variable", "replacement_reserve", reserve_pct * total_rev))
    for k, v in per_stay.items():
        lines.append(("per_stay", k, v * stays))
    for k, v in fixed.items():
        lines.append(("fixed", k, v))

    opex = sum(x[2] for x in lines)
    noi = total_rev - opex
    fixed_total = sum(fixed.values())
    pct_total = sum(pct_costs.values()) + reserve_pct
    per_stay_total = sum(per_stay.values())

    # break-even: nights where NOI = 0 at today's ADR and stay length
    rev_per_night = adr + cleaning_fee_per_stay / los + other_per_night
    contrib_per_night = rev_per_night * (1 - pct_total) - per_stay_total / los
    breakeven_nights = fixed_total / contrib_per_night if contrib_per_night > 0 else None

    out = {
        "booked_nights": booked,
        "available_nights": available,
        "stays": stays,
        "avg_stay": los,
        "occupancy": booked / available,
        "adr": adr,
        "revpar": rent / available,
        "rent": rent,
        "cleaning_fees": cleaning_fees,
        "other_income": other,
        "total_revenue": total_rev,
        "cost_lines": lines,
        "opex": opex,
        "opex_ratio": opex / total_rev,
        "noi": noi,
        "noi_margin": noi / total_rev,
        "fixed_total": fixed_total,
        "pct_total": pct_total,
        "per_stay_total": per_stay_total,
        "rev_per_night": rev_per_night,
        "contrib_per_night": contrib_per_night,
        "breakeven_nights": breakeven_nights,
        "breakeven_occ": breakeven_nights / available if breakeven_nights else None,
    }

    if p.get("self_managed"):
        mkt = p.get("market_mgmt_pct", 0.20)
        out["noi_with_manager"] = noi - mkt * total_rev
    val = p.get("value", {})
    total_value = val.get("property", {}).get("amount", 0) + val.get("ffe", {}).get("amount", 0)
    out["total_value"] = total_value or None
    out["cap_rate"] = noi / total_value if total_value else None
    if p.get("self_managed") and total_value:
        out["cap_rate_with_manager"] = out["noi_with_manager"] / total_value
    debt = p.get("annual_debt_service")
    if debt is not None:
        out["cash_flow_after_debt"] = noi - debt
    return out


def required_to_hit(p, base, noi_goal):
    """Occupancy needed at today's ADR, and ADR needed at target occupancy."""
    los = base["avg_stay"]
    rev = p["revenue"]
    stays0 = rev.get("stays") or rev["booked_nights"] / rev["avg_stay_nights"]
    cf_per_stay = rev.get("cleaning_fees", 0.0) / stays0
    other_per_night = rev.get("other_income", 0.0) / rev["booked_nights"]
    k = 1 - base["pct_total"]
    fixed = base["fixed_total"]
    # occupancy at current ADR
    nights_needed = (noi_goal + fixed) / base["contrib_per_night"] if base["contrib_per_night"] > 0 else None
    occ_needed = nights_needed / base["available_nights"] if nights_needed else None
    # ADR at a given number of nights N: NOI = N*(adr + cf/los + o)*k - N*ps/los - fixed
    return occ_needed, (lambda N: ((noi_goal + fixed + N * base["per_stay_total"] / los) / (N * k)) - cf_per_stay / los - other_per_night)


def nice(key):
    words = key.replace("_", " ").split()
    up = {"str": "STR", "hoa": "HOA", "ffe": "FF&E", "ota": "OTA"}
    words = [up.get(w.lower(), w) for w in words]
    out = " ".join(words)
    return out[0].upper() + out[1:]


def flags_for(p, m):
    """Plain-language flags and the playbook step that fixes each."""
    flags = []
    tot = m["total_revenue"]
    mkt = p.get("market", {})
    if mkt.get("occupancy") and m["occupancy"] < mkt["occupancy"] - 0.03:
        flags.append((f"Occupancy {pct(m['occupancy'])} is below the market's {pct(mkt['occupancy'])}.",
                      [4, 5, 6]))
    busy = mkt.get("occupancy") and m["occupancy"] > mkt["occupancy"] + 0.03
    if busy and mkt.get("adr") and m["adr"] < mkt["adr"]:
        flags.append((f"Occupancy {pct(m['occupancy'])} beats the market's {pct(mkt['occupancy'])} while the nightly rate "
                      f"{money(m['adr'])} trails its {money(mkt['adr'])}, so prices are probably too low. "
                      "Rate is the lever here, not more nights.", [7]))
    elif mkt.get("adr") and m["adr"] < mkt["adr"] * 0.95:
        flags.append((f"Average nightly rate {money(m['adr'])} is below the market's {money(mkt['adr'])}.", [7, 4]))

    groups = {"management": 0.0, "platform": 0.0, "utilities": 0.0, "repairs": 0.0, "reserve": 0.0}
    cleaning_cost = 0.0
    for kind, key, amt in m["cost_lines"]:
        k = key.lower()
        if "manage" in k:
            groups["management"] += amt
        elif "platform" in k or "airbnb" in k or "vrbo" in k or "ota" in k:
            groups["platform"] += amt
        elif k in UTILITY_KEYS:
            groups["utilities"] += amt
        elif k in REPAIR_KEYS:
            groups["repairs"] += amt
        elif k == "replacement_reserve":
            groups["reserve"] += amt
        if "clean" in k or "laundry" in k or "linen" in k:
            cleaning_cost += amt
    for g, amt in groups.items():
        lo, hi, why = BENCHMARKS[g]
        if g == "management" and p.get("self_managed"):
            continue
        if amt and amt / tot > hi:
            step = [5] if g == "platform" else [9] if g in ("repairs",) else []
            flags.append((f"{nice(g)} is {pct(amt / tot)} of revenue, above the usual top of {pct(hi, 0)}. {why}", step))
    if cleaning_cost and m["cleaning_fees"] and cleaning_cost > m["cleaning_fees"] * 1.05:
        flags.append((f"Cleaning and laundry cost {money(cleaning_cost)} but cleaning fees bring in {money(m['cleaning_fees'])}. "
                      "Raise the fee or renegotiate the turnover rate.", [7]))
    if m["noi_margin"] < NOI_MARGIN_FLOOR:
        flags.append((f"NOI margin is {pct(m['noi_margin'])}. Below about {pct(NOI_MARGIN_FLOOR, 0)}, one bad month or repair "
                      "wipes out the year, so costs need a line-by-line review.", []))
    if p.get("self_managed") and "noi_with_manager" in m and m["noi_with_manager"] < 0.5 * m["noi"]:
        flags.append((f"Most of this property's NOI is really your own unpaid labor: with a paid manager it drops to "
                      f"{money(m['noi_with_manager'])}. Count your hours before you buy the next one.", []))
    if m["breakeven_occ"] and m["breakeven_occ"] > 0.55:
        flags.append((f"Break-even occupancy is {pct(m['breakeven_occ'])}. A slow season can push this property into a loss.", [6, 7]))
    return flags


def default_levers(p, scenario, settings):
    base = settings.get(scenario, {})
    mkt = p.get("market", {})
    lv = {
        "occ_pts": base.get("occ_pts", 5 if scenario == "target" else 10),
        "adr_pct": base.get("adr_pct", 5 if scenario == "target" else 10),
        "cost_cut_pct": base.get("cost_cut_pct", 0 if scenario == "target" else 3),
        "occ_cap": OCC_CEILING,
        "adr_cap": None,
    }
    if mkt.get("occupancy"):
        lv["occ_cap"] = min(OCC_CEILING, mkt["occupancy"] + (0.05 if scenario == "target" else 0.10))
    if mkt.get("adr"):
        lv["adr_cap"] = mkt["adr"] * (1.05 if scenario == "target" else 1.15)
    lv.update(p.get("levers", {}).get(scenario, {}))
    return lv


def build(data):
    props = data["properties"]
    settings = data.get("lever_settings", {})
    results = []
    for p in props:
        base = property_model(p)
        tgt_lv = default_levers(p, "target", settings)
        str_lv = default_levers(p, "stretch", settings)
        target = property_model(p, tgt_lv)
        stretch = property_model(p, str_lv)
        results.append({"p": p, "base": base, "target": target, "stretch": stretch,
                        "levers": {"target": tgt_lv, "stretch": str_lv}, "flags": flags_for(p, base)})

    def roll(key):
        r = {}
        for f in ("total_revenue", "opex", "noi", "rent", "booked_nights", "available_nights"):
            r[f] = sum(x[key][f] for x in results)
        vals = [x[key]["total_value"] for x in results]
        r["total_value"] = sum(v for v in vals if v) if all(vals) else None
        r["occupancy"] = r["booked_nights"] / r["available_nights"]
        r["adr"] = r["rent"] / r["booked_nights"]
        r["noi_margin"] = r["noi"] / r["total_revenue"]
        r["opex_ratio"] = r["opex"] / r["total_revenue"]
        r["cap_rate"] = r["noi"] / r["total_value"] if r["total_value"] else None
        return r

    portfolio = {k: roll(k) for k in ("base", "target", "stretch")}

    goal = data.get("goals", {})
    goal_noi = goal.get("portfolio_noi")
    if goal_noi is None and goal.get("portfolio_cap_rate") and portfolio["base"]["total_value"]:
        goal_noi = goal["portfolio_cap_rate"] * portfolio["base"]["total_value"]
    goal_view = None
    if goal_noi is not None:
        tgt_noi_total = portfolio["target"]["noi"]
        per = []
        for x in results:
            share = (x["target"]["noi"] / tgt_noi_total) if tgt_noi_total > 0 else 1 / len(results)
            g = goal_noi * share
            occ_needed, adr_at = required_to_hit(x["p"], x["base"], g)
            adr_needed = adr_at(x["target"]["booked_nights"])
            cap_occ = x["levers"]["stretch"]["occ_cap"]
            mkt_adr = x["p"].get("market", {}).get("adr")
            stretchy = (occ_needed is None or occ_needed > cap_occ) and (mkt_adr and adr_needed > mkt_adr * 1.2)
            per.append({"name": x["p"]["name"], "noi_goal": g, "occ_needed": occ_needed,
                        "adr_needed_at_target_occ": adr_needed, "target_occ": x["target"]["occupancy"],
                        "out_of_reach": bool(stretchy)})
        verdict = ("within the realistic target" if goal_noi <= portfolio["target"]["noi"]
                   else "between target and stretch" if goal_noi <= portfolio["stretch"]["noi"]
                   else "beyond the stretch case")
        goal_view = {"noi": goal_noi, "per_property": per, "verdict": verdict,
                     "gap_vs_today": goal_noi - portfolio["base"]["noi"]}

    return {"results": results, "portfolio": portfolio, "goal": goal_view}


def monthly_split(p, annual_rev):
    seas = p.get("monthly_revenue_last_year")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if seas and len(seas) == 12 and sum(seas) > 0:
        tot = sum(seas)
        return [(m, annual_rev * s / tot) for m, s in zip(months, seas)], "last year's monthly pattern"
    return [(m, annual_rev / 12) for m in months], "an even split (add last year's monthly revenue to shape this)"


def render_md(data, out):
    biz = data.get("business", {})
    goal = data.get("goals", {})
    P = out["portfolio"]
    L = []
    L.append(f"# Business Brain: {biz.get('name', 'My STR business')}")
    L.append("")
    L.append(f"_Built with The Brain kit (STR Booster playbook, step 1) on {data.get('as_of', '')}. "
             f"Numbers cover {data.get('period', 'the last 12 months')}. "
             "Every later step reads this file. \"Est.\" marks an estimate, not a fact._")
    L.append("")
    L.append("## 1. Goals for the next 12 months")
    L.append("")
    for g in goal.get("statements", []):
        L.append(f"- {g}")
    if goal.get("portfolio_noi"):
        L.append(f"- Portfolio NOI goal: **{money(goal['portfolio_noi'])}** a year.")
    if goal.get("portfolio_cap_rate"):
        L.append(f"- Portfolio cap rate goal: **{pct(goal['portfolio_cap_rate'])}**.")
    L.append("")

    L.append("## 2. Portfolio at a glance")
    L.append("")
    b = P["base"]
    L.append("| | Today | Target (12 mo) | Stretch |")
    L.append("|---|---:|---:|---:|")
    rows = [("Revenue", "total_revenue", money), ("Operating costs", "opex", money), ("**NOI**", "noi", money),
            ("NOI margin", "noi_margin", pct), ("Occupancy", "occupancy", pct), ("Average nightly rate", "adr", money),
            ("Cap rate", "cap_rate", pct)]
    for name, key, f in rows:
        L.append(f"| {name} | {f(P['base'][key])} | {f(P['target'][key])} | {f(P['stretch'][key])} |")
    if b["total_value"]:
        any_est = any(r["p"].get("value", {}).get(k, {}).get("est") for r in out["results"] for k in ("property", "ffe"))
        L.append("")
        L.append(f"Total value, property plus contents: **{label(money(b['total_value']), any_est)}**.")
    if out["goal"]:
        g = out["goal"]
        L.append("")
        L.append(f"**Goal check:** the NOI goal of {money(g['noi'])} is {money(g['gap_vs_today'])} above today and "
                 f"**{g['verdict']}**.")
    if goal.get("portfolio_cap_rate") and P["base"]["cap_rate"] is not None:
        cg = goal["portfolio_cap_rate"]
        where = ("already met" if P["base"]["cap_rate"] >= cg else "met by the target" if P["target"]["cap_rate"] >= cg
                 else "met by the stretch case" if P["stretch"]["cap_rate"] >= cg else "not met even in the stretch case")
        need = cg * P["base"]["total_value"]
        L.append("")
        L.append(f"**Cap rate check:** the {pct(cg)} goal needs about {money(need)} of NOI on today's value, and is **{where}**.")
    L.append("")

    L.append("## 3. Property by property")
    for r in out["results"]:
        p, m, t, s = r["p"], r["base"], r["target"], r["stretch"]
        val = p.get("value", {})
        L.append("")
        L.append(f"### {p['name']}")
        L.append("")
        desc = ", ".join(x for x in [p.get("location"), p.get("type"),
                                      f"{p['bedrooms']} bed" if p.get("bedrooms") else None,
                                      f"sleeps {p['sleeps']}" if p.get("sleeps") else None,
                                      "self-managed" if p.get("self_managed") else "professionally managed"] if x)
        L.append(desc + ".")
        L.append("")
        L.append("**Revenue**")
        L.append("")
        L.append(f"- {m['booked_nights']:.0f} of {m['available_nights']:.0f} nights booked, occupancy {pct(m['occupancy'])}, "
                 f"{m['stays']:.0f} stays averaging {m['avg_stay']:.1f} nights.")
        L.append(f"- Average nightly rate {money(m['adr'])}, RevPAR {money(m['revpar'])}.")
        L.append(f"- Rent {money(m['rent'])} + cleaning fees {money(m['cleaning_fees'])} + other {money(m['other_income'])} "
                 f"= **{money(m['total_revenue'])}**.")
        L.append("")
        L.append("**Costs**")
        L.append("")
        L.append("| Cost | Type | Annual | % of revenue |")
        L.append("|---|---|---:|---:|")
        kinds = {"variable": "% of revenue", "per_stay": "Per stay", "fixed": "Fixed"}
        for kind, key, amt in m["cost_lines"]:
            L.append(f"| {nice(key)} | {kinds[kind]} | {money(amt)} | {pct(amt / m['total_revenue'])} |")
        L.append(f"| **Total** | | **{money(m['opex'])}** | **{pct(m['opex_ratio'])}** |")
        L.append("")
        L.append(f"**NOI: {money(m['noi'])}** ({pct(m['noi_margin'])} margin).")
        if "noi_with_manager" in m:
            L.append(f"If you paid a manager {pct(p.get('market_mgmt_pct', 0.20), 0)}, NOI would be {money(m['noi_with_manager'])}. "
                     "That is the number a buyer or lender would use.")
        if "cash_flow_after_debt" in m:
            L.append(f"After {money(p['annual_debt_service'])} of mortgage payments, cash flow is {money(m['cash_flow_after_debt'])}.")
        L.append("")
        L.append("**Value and cap rate**")
        L.append("")
        pv, fv = val.get("property", {}), val.get("ffe", {})
        if pv:
            L.append(f"- Property: {label(money(pv['amount']), pv.get('est'))}. Source: {pv.get('source', 'owner')}.")
        if fv:
            L.append(f"- Contents and FF&E: {label(money(fv['amount']), fv.get('est'))}. Source: {fv.get('source', 'owner')}.")
        if m["cap_rate"] is not None:
            est = pv.get("est") or fv.get("est")
            L.append(f"- Total {label(money(m['total_value']), est)}, so the **cap rate is {pct(m['cap_rate'])}**"
                     + (f" ({pct(m['cap_rate_with_manager'])} with a paid manager)." if "cap_rate_with_manager" in m else "."))
        L.append(f"- Break-even occupancy: {pct(m['breakeven_occ'])} at today's rate." if m["breakeven_occ"]
                 else "- Break-even: not reachable at today's rate and costs.")
        L.append("")
        L.append("**Targets**")
        L.append("")
        L.append("| | Floor (break-even) | Today | Target (12 mo) | Stretch |")
        L.append("|---|---:|---:|---:|---:|")
        be = m["breakeven_occ"]
        L.append(f"| Occupancy | {pct(be)} | {pct(m['occupancy'])} | {pct(t['occupancy'])} | {pct(s['occupancy'])} |")
        L.append(f"| Average nightly rate | {money(m['adr'])} | {money(m['adr'])} | {money(t['adr'])} | {money(s['adr'])} |")
        L.append(f"| Revenue | {money(m['rev_per_night'] * m['breakeven_nights']) if be else 'n/a'} | {money(m['total_revenue'])} | {money(t['total_revenue'])} | {money(s['total_revenue'])} |")
        L.append(f"| Cost ratio | 100% | {pct(m['opex_ratio'])} | {pct(t['opex_ratio'])} | {pct(s['opex_ratio'])} |")
        L.append(f"| NOI | $0 | {money(m['noi'])} | {money(t['noi'])} | {money(s['noi'])} |")
        if m["cap_rate"] is not None:
            L.append(f"| Cap rate | 0.0% | {pct(m['cap_rate'])} | {pct(t['cap_rate'])} | {pct(s['cap_rate'])} |")
        tl, sl = r["levers"]["target"], r["levers"]["stretch"]
        L.append("")
        L.append(f"Target assumes up to +{tl['occ_pts']} occupancy points and +{tl['adr_pct']}% rate"
                 + (f", capped near the market" if p.get("market") else "") +
                 f". Stretch assumes up to +{sl['occ_pts']} points, +{sl['adr_pct']}% rate and {sl['cost_cut_pct']}% lower fixed and per-stay costs.")
        months, how = monthly_split(p, t["total_revenue"])
        L.append("")
        L.append(f"Monthly revenue target, using {how}: " + ", ".join(f"{mo} {money(v)}" for mo, v in months) + ".")
        if out["goal"]:
            gp = next(x for x in out["goal"]["per_property"] if x["name"] == p["name"])
            occ_txt = pct(gp["occ_needed"]) if gp["occ_needed"] else "n/a"
            L.append("")
            L.append(f"To carry its share of the goal ({money(gp['noi_goal'])} NOI), this property needs **{occ_txt} occupancy at today's rate**, "
                     f"or **{money(gp['adr_needed_at_target_occ'])} a night at {pct(gp['target_occ'])} occupancy**."
                     + (" That is out of reach on rate and occupancy alone, so costs or the goal need to move." if gp["out_of_reach"] else ""))
        if r["flags"]:
            L.append("")
            L.append("**Worth a look**")
            L.append("")
            for text, steps in r["flags"]:
                tail = (" Fix in " + " and ".join(PLAYBOOK[s] for s in steps) + ".") if steps else ""
                L.append(f"- {text}{tail}")
    L.append("")
    L.append("## 4. Strategies (first draft)")
    L.append("")
    by_step = {}
    for r in out["results"]:
        for text, steps in r["flags"]:
            by_step.setdefault(steps[0] if steps else 0, []).append(r["p"]["name"])
    if by_step:
        for st in sorted(by_step):
            names = ", ".join(sorted(set(by_step[st])))
            what = PLAYBOOK.get(st, "Costs and operations (line-by-line review)")
            L.append(f"- {what}: {names}.")
    else:
        L.append("- No big gaps found. Protect the rate and keep costs where they are.")
    L.append("")
    L.append("## 5. The numbers we watch")
    L.append("")
    L.append("Check monthly against the Target column: occupancy, average nightly rate, RevPAR, total revenue, "
             "cost ratio and NOI per property. Re-run The Brain each quarter with fresh numbers.")
    L.append("")
    L.append("## 6. How later steps use this file")
    L.append("")
    L.append("- Step 4 (listings) and step 6 (marketing) start with the properties flagged for low occupancy.")
    L.append("- Step 7 (revenue management) uses the rate and occupancy targets and the break-even floor as the minimum price guardrail.")
    L.append("- Step 8 (win more homes) uses NOI, cap rate and the paid-manager view to show owners what a property earns.")
    L.append("- Step 9 (guest experience) uses the repairs, cleaning and reserve lines to keep standards up without blowing the budget.")
    L.append("")
    L.append("## 7. Definitions")
    L.append("")
    L.append("- **NOI (net operating income):** revenue minus operating costs. It leaves out mortgage payments, depreciation, income tax and big one-off improvements.")
    L.append("- **Cap rate:** NOI divided by what the property and its contents are worth. It is the yield on the asset if you owned it outright.")
    L.append("- **Break-even occupancy:** the occupancy where revenue just covers costs at today's nightly rate.")
    L.append("- **Replacement reserve:** money set aside each year for furniture, linens and appliances that wear out.")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--md", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()
    with open(a.data) as f:
        data = json.load(f)
    out = build(data)
    md = render_md(data, out)
    with open(a.md, "w") as f:
        f.write(md)
    if a.json:
        slim = {"portfolio": out["portfolio"], "goal": out["goal"],
                "properties": [{"name": r["p"]["name"], "today": {k: v for k, v in r["base"].items() if k != "cost_lines"},
                                "target": {k: v for k, v in r["target"].items() if k != "cost_lines"},
                                "stretch": {k: v for k, v in r["stretch"].items() if k != "cost_lines"},
                                "flags": [t for t, _ in r["flags"]]} for r in out["results"]]}
        with open(a.json, "w") as f:
            json.dump(slim, f, indent=2, default=float)
    b = out["portfolio"]["base"]
    print(f"Portfolio today: revenue {money(b['total_revenue'])}, NOI {money(b['noi'])}, cap rate {pct(b['cap_rate'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
