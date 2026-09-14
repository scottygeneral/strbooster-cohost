const reply=(statusCode,body)=>({statusCode,headers:{'Content-Type':'application/json','Cache-Control':'no-store'},body:JSON.stringify(body)});
exports.handler=async event=>{
 if(event.httpMethod!=='POST')return reply(405,{ok:false,error:'Use the waitlist form.'});
 let d;try{if(!event.body||event.body.length>8192)throw Error();d=JSON.parse(event.body);}catch{return reply(400,{ok:false,error:'Invalid form data.'});}
 if(!d||typeof d.name!=='string'||!d.name.trim()||d.name.length>120||typeof d.email!=='string'||d.email.length>254||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)||!Number.isInteger(d.property_count)||d.property_count<1||d.property_count>10000||d.consent!==true)return reply(400,{ok:false,error:'Check your name, email, property count and consent.'});
 const name=d.name.trim(),[first_name,...last]=name.split(/\s+/);
 const incoming=d.attribution&&typeof d.attribution==='object'?d.attribution:{};
 const attribution={};
 for(const key of ['utm_source','utm_medium','utm_campaign','utm_content','utm_term']){
  attribution[key]=typeof incoming[key]==='string'?incoming[key].replace(/[\u0000-\u001f\u007f]/g,'').slice(0,150):'';
 }
 attribution.landing_page='';
 try{const url=new URL(incoming.landing_page);if(['https:','http:'].includes(url.protocol)&&['strbooster.com','www.strbooster.com'].includes(url.hostname))attribution.landing_page=(url.origin+url.pathname).slice(0,500);}catch{}
 attribution.referring_host=typeof incoming.referring_host==='string'&&/^[a-z0-9.-]{1,253}$/i.test(incoming.referring_host)?incoming.referring_host:'';
 const payload={name,first_name,last_name:last.join(' '),email:d.email.trim(),property_count:d.property_count,source:'STR Booster website',interest:'52Rev beta waitlist',form_id:'52rev-beta-waitlist',consent:true,consent_text:'Email me about 52Rev beta access and updates. I can unsubscribe at any time.',submitted_at:new Date().toISOString(),test_submission:false,...attribution};
 try{const r=await fetch('https://services.leadconnectorhq.com/hooks/VYmmcd3zhhauMLyqAUSb/webhook-trigger/969585e8-6a27-49b9-8bfa-6f3a6158055b',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:AbortSignal.timeout(10000)});return r.ok?reply(200,{ok:true}):reply(502,{ok:false,error:'Submission could not be confirmed.'});}catch{return reply(502,{ok:false,error:'Submission could not be confirmed.'});}
};
