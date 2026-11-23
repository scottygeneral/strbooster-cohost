/* Free playbook page: HighLevel form embed plus a soft kit unlock.
   Signups go straight into HighLevel through the embedded form. Without JavaScript the kit links download directly. */
(()=>{
 const KEY='strbooster-playbook-unlocked';
 const note=document.querySelector('#pb-unlock-note');
 const box=document.querySelector('#get-the-kits');
 const status=box?.querySelector('.pb-status');
 const track=(name,details={})=>window.strBoosterTrack?.(name,{form_id:'free-playbook',lead_type:'newsletter',...details});
 let unlocked=false;
 try{unlocked=localStorage.getItem(KEY)==='1';}catch{}
 const setUnlocked=(source)=>{
  if(!unlocked&&source)track('generate_lead',{method:source});
  unlocked=true;
  try{localStorage.setItem(KEY,'1');}catch{}
  document.body.classList.remove('pb-locked');
  document.body.classList.add('pb-unlocked');
  if(note)note.textContent='Downloads unlocked. Thanks for joining.';
  if(status&&source)status.innerHTML='You’re in. The downloads are unlocked: <a href="#kits">get the kits</a>.';
 };
 if(unlocked)setUnlocked();
 else document.body.classList.add('pb-locked');

 // HighLevel's embedded form posts messages to the page; a submit message unlocks the kits.
 addEventListener('message',event=>{
  if(!/(leadconnectorhq\.com|msgsndr\.com)$/.test(new URL(event.origin||'http://x').hostname))return;
  const text=typeof event.data==='string'?event.data:JSON.stringify(event.data||'');
  if(/submit|set-sticky-contacts/i.test(text))setUnlocked('highlevel_form');
 });

 document.querySelectorAll('.pb-unlock').forEach(b=>b.addEventListener('click',()=>{setUnlocked('self_confirm');status?.focus();}));

 document.querySelectorAll('[data-kit]').forEach(link=>link.addEventListener('click',event=>{
  if(unlocked){track('kit_download',{kit:link.dataset.kit});return;}
  event.preventDefault();
  box?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
  if(status)status.textContent='Subscribe here and the '+(link.closest('article,li')?.querySelector('h3,h4')?.textContent.trim().replace(/^Use the /,'')||'kit')+' download unlocks.';
 }));
})();
