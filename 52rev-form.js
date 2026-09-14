const form=document.querySelector('#rev-waitlist'),status=document.querySelector('#rev-status'),submit=form.querySelector('[type=submit]');
let sending=false,started=false;
const measure=(name)=>window.strBoosterTrack?.(name,{form_id:'52rev-beta-waitlist',lead_type:'52rev_beta'});
form.addEventListener('input',()=>{if(!started){started=true;measure('form_start');}});
async function send(data){
 if(sending)return;sending=true;submit.disabled=true;status.textContent='Sending…';
 try{const r=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),signal:AbortSignal.timeout(20000)});const result=await r.json();if(!r.ok||!result.ok)throw new Error(result.error||'Submission could not be confirmed.');
 status.textContent='You’re on the waiting list. We’ll email you when beta access becomes available.';
 measure('generate_lead');
 form.reset();started=false;
 }catch(e){measure('lead_submission_error');status.textContent='Submission could not be confirmed. Please retry or contact david@strbooster.com. Your details have been kept.';}
 finally{sending=false;submit.disabled=false;status.focus();}
}
form.addEventListener('submit',e=>{e.preventDefault();if(!form.reportValidity())return;const d=new FormData(form);send({name:d.get('name'),email:d.get('email'),property_count:Number(d.get('property_count')),consent:d.get('consent')==='on',attribution:window.strBoosterAttribution?.()||{}})});
