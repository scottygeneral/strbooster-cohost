const form=document.querySelector('#rev-waitlist'),status=document.querySelector('#rev-status'),test=document.querySelector('#rev-test'),submit=form.querySelector('[type=submit]');
test.hidden=new URLSearchParams(location.search).get('test')!=='52rev';
let sending=false;
async function send(data,isTest){
 if(sending)return;sending=true;submit.disabled=true;test.disabled=true;status.textContent='Sending…';
 try{const r=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...data,test_submission:isTest}),signal:AbortSignal.timeout(20000)});const result=await r.json();if(!r.ok||!result.ok)throw new Error(result.error||'Submission could not be confirmed.');
 status.textContent=isTest?'Test payload received by GoHighLevel. Capture the reference request in your workflow trigger.':'You’re on the waiting list. We’ll email you when beta access becomes available.';
 if(!isTest)form.reset();
 }catch(e){status.textContent='Submission could not be confirmed. Please retry or contact david@strbooster.com. Your details have been kept.';}
 finally{sending=false;submit.disabled=false;test.disabled=false;status.focus();}
}
form.addEventListener('submit',e=>{e.preventDefault();if(!form.reportValidity())return;const d=new FormData(form);send({name:d.get('name'),email:d.get('email'),property_count:Number(d.get('property_count')),consent:d.get('consent')==='on'},false)});
test.addEventListener('click',()=>send({name:'52Rev Test Lead',email:'52rev-test@example.com',property_count:2,consent:true},true));
