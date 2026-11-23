/* Free playbook page: email signup (HighLevel via Netlify function) and kit unlock.
   Without JavaScript the kit links download directly and the form posts normally. */
(()=>{
 const KEY='strbooster-playbook-unlocked';
 const forms=[...document.querySelectorAll('.pb-form')];
 const note=document.querySelector('#pb-unlock-note');
 const track=(name,details={})=>window.strBoosterTrack?.(name,{form_id:'free-playbook',lead_type:'newsletter',...details});
 let unlocked=false;
 try{unlocked=localStorage.getItem(KEY)==='1';}catch{}
 const setUnlocked=()=>{
  unlocked=true;
  try{localStorage.setItem(KEY,'1');}catch{}
  document.body.classList.add('pb-unlocked');
  if(note)note.textContent='Downloads unlocked. Thanks for joining.';
 };
 if(unlocked)setUnlocked();
 else document.body.classList.add('pb-locked');

 document.querySelectorAll('[data-kit]').forEach(link=>link.addEventListener('click',event=>{
  if(unlocked){track('kit_download',{kit:link.dataset.kit});return;}
  event.preventDefault();
  const target=document.querySelector('#get-the-kits');
  target?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
  const status=target?.querySelector('.pb-status');
  if(status)status.textContent='Enter your email and the '+link.closest('article,li')?.querySelector('h3,h4')?.textContent.trim().replace(/^Use the /,'')+' download unlocks right away.';
  setTimeout(()=>target?.querySelector('input[type=email]')?.focus({preventScroll:true}),400);
 }));

 forms.forEach(form=>{
  const status=form.querySelector('.pb-status'),submit=form.querySelector('[type=submit]');
  let sending=false,started=false;
  form.addEventListener('input',()=>{if(!started){started=true;track('form_start');}});
  form.addEventListener('submit',async event=>{
   event.preventDefault();
   if(sending)return;
   const email=form.querySelector('input[type=email]'),consent=form.querySelector('input[name=consent]');
   if(!email.value.trim()||!email.checkValidity()){status.textContent='Please enter a valid email address.';email.focus();return;}
   if(!consent.checked){status.textContent='Please tick the box so we can send you the kits.';consent.focus();return;}
   const d=new FormData(form);
   sending=true;submit.disabled=true;status.textContent='Sending…';
   try{
    const r=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json'},signal:AbortSignal.timeout(20000),
     body:JSON.stringify({first_name:d.get('first_name')||'',email:d.get('email'),role:d.get('role'),company:d.get('company')||'',consent:true,attribution:window.strBoosterAttribution?.()||{}})});
    const result=await r.json().catch(()=>({}));
    if(!r.ok||!result.ok)throw new Error(result.error||'failed');
    setUnlocked();
    track('generate_lead');
    form.reset();started=false;
    status.innerHTML='You’re in. The downloads are unlocked: <a href="#kits">get the kits</a>. Check your inbox for a welcome email.';
   }catch{
    track('lead_submission_error');
    status.textContent='We could not confirm your signup. Please try again, or email info@strbooster.com and we will send the kits.';
   }finally{sending=false;submit.disabled=false;status.focus();}
  });
 });
})();
