/* Newsletter form: posts to /.netlify/functions/newsletter-signup and shows the result in place. */
(()=>{
 const track=(n,d={})=>window.strBoosterTrack?.(n,d);
 const params=new URLSearchParams(location.search);
 document.querySelectorAll('form.sb-signup').forEach(form=>{
  const status=form.querySelector('.sb-signup-status');
  const button=form.querySelector('button[type=submit]');
  const show=(ok,msg)=>{status.textContent=msg;status.dataset.state=ok?'ok':'error';};
  if(params.get('signup')==='ok')show(true,'You’re in. Check your inbox for the welcome email.');
  if(params.get('signup')==='error')show(false,'Something went wrong. Please try again.');
  form.addEventListener('submit',async e=>{
   e.preventDefault();
   if(!form.reportValidity())return;
   const data=Object.fromEntries(new FormData(form));
   button.disabled=true;const label=button.textContent;button.textContent='Sending…';show(true,'');
   try{
    const r=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data)});
    const j=await r.json().catch(()=>({}));
    if(r.ok&&j.ok){form.classList.add('is-done');show(true,j.message||'You’re in.');track('newsletter_signup',{page:data.page});}
    else show(false,j.message||'Something went wrong. Please try again.');
   }catch{show(false,'Couldn’t reach the server. Check your connection and try again.');}
   button.disabled=false;button.textContent=label;
  });
 });
})();
