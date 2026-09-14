const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('.nav-links');
function closeNav(){nav?.classList.remove('open');toggle?.setAttribute('aria-expanded','false');}
toggle?.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});
const groups=[...document.querySelectorAll('.nav-group')];
groups.forEach(group=>group.addEventListener('toggle',()=>{if(group.open)groups.forEach(other=>{if(other!==group)other.open=false;});}));
document.addEventListener('click',event=>{if(!event.target.closest('.nav-group'))groups.forEach(group=>group.open=false);if(!event.target.closest('.site-header'))closeNav();});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){const active=groups.find(group=>group.open);groups.forEach(group=>group.open=false);if(active)active.querySelector('summary').focus();else if(nav?.classList.contains('open')){closeNav();toggle.focus();}}});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeNav));
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{const filter=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));let count=0;document.querySelectorAll('[data-category]').forEach(card=>{card.hidden=filter!=='all'&&card.dataset.category!==filter;if(!card.hidden)count++;});const status=document.querySelector('#filter-status');if(status)status.textContent=`${count} resources shown`;}));

/* STR Booster measurement: send action events to the existing GA4 destination.
   Do not add matching GTM click/form tags: these events are already sent here. */
(()=>{
 const GA_ID='G-YQ9L9GHV31',KEY='strbooster-attribution-v1';
 const fields=['utm_source','utm_medium','utm_campaign','utm_content','utm_term'];
 const clean=value=>typeof value==='string'?value.replace(/[\u0000-\u001f\u007f]/g,'').slice(0,150):'';
 const params=new URLSearchParams(location.search);
 let attribution={};
 try{const saved=JSON.parse(sessionStorage.getItem(KEY)||'null');if(saved&&Date.now()-saved.updated_at<30*60*1000)attribution=saved.data||{};}catch{}
 const campaign=Object.fromEntries(fields.map(key=>[key,clean(params.get(key))]));
 if(!attribution.landing_page||campaign.utm_source){
  let referring_host='';try{referring_host=new URL(document.referrer).hostname;}catch{}
  attribution={...campaign,landing_page:location.origin+location.pathname,referring_host};
 }
 try{sessionStorage.setItem(KEY,JSON.stringify({updated_at:Date.now(),data:attribution}));}catch{}
 window.strBoosterAttribution=()=>({...attribution});
 window.strBoosterTrack=(name,details={})=>{
  try{if(typeof window.gtag==='function')window.gtag('event',name,{...details,send_to:GA_ID,transport_type:'beacon',page_path:location.pathname});}catch{}
 };
 document.addEventListener('click',event=>{
  const link=event.target.closest('a[href]');if(!link)return;
  let url;try{url=new URL(link.href,location.href);}catch{return;}
  const locationName=link.closest('.site-header')?'navigation':link.closest('.site-footer')?'footer':link.closest('.page-hero,.hero')?'hero':'content';
  const detail={button_location:locationName};
  if(url.hostname==='my.hostgrowthhub.com'&&url.pathname.startsWith('/communities/')){
   window.strBoosterTrack('community_click',detail);
  }else if(url.hostname==='links.strbooster.com'&&url.pathname.includes('/widget/booking/')){
   window.strBoosterTrack('booking_click',detail);
  }else if(url.hostname==='guest-intel.strbooster.com'){
   window.strBoosterTrack('app_click',{...detail,app_name:'guest_intel'});
  }else if(url.protocol==='mailto:'){
   const card=link.closest('article');
   const partner=location.pathname.includes('tools-partners')?card?.querySelector('h2,h3')?.textContent.trim():undefined;
   window.strBoosterTrack('contact_click',{...detail,contact_method:'email',...(partner?{partner_name:partner}:{})});
  }else if(link.rel.split(/\s+/).includes('sponsored')){
   const partner=link.closest('article')?.querySelector('h2,h3')?.textContent.trim();
   if(partner)window.strBoosterTrack('affiliate_click',{...detail,partner_name:partner});
  }else if(url.origin===location.origin&&url.pathname==='/get-expert-help.html'){
   window.strBoosterTrack('service_enquiry_click',{...detail,service:clean(url.searchParams.get('service'))||'general'});
  }
 });
})();

/* Load the shared HighLevel chat widget once on every page. */
(()=>{
 const widgetId='6aa7fb1fef660e70afde2470';
 if(document.querySelector('script[data-widget-id="'+widgetId+'"]'))return;
 const script=document.createElement('script');
 script.src='https://widgets.leadconnectorhq.com/loader.js';
 script.dataset.resourcesUrl='https://widgets.leadconnectorhq.com/chat-widget/loader.js';
 script.dataset.widgetId=widgetId;
 script.async=true;
 document.body.appendChild(script);
})();
