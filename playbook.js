/* Free journey page: copy-prompt buttons and download tracking. Nothing is gated. */
(()=>{
 const track=(name,details={})=>window.strBoosterTrack?.(name,{form_id:'free-playbook',...details});
 document.querySelectorAll('.pb-copy').forEach(button=>button.addEventListener('click',async()=>{
  const text=document.getElementById(button.dataset.copy)?.textContent||'';
  try{await navigator.clipboard.writeText(text);button.textContent='Copied';}
  catch{const r=document.createRange();r.selectNodeContents(document.getElementById(button.dataset.copy));const s=getSelection();s.removeAllRanges();s.addRange(r);button.textContent='Selected: press copy';}
  track('prompt_copy',{prompt:button.dataset.copy});
  setTimeout(()=>{button.textContent='Copy prompt';},2200);
 }));
 document.querySelectorAll('[data-kit]').forEach(link=>link.addEventListener('click',()=>track('kit_download',{kit:link.dataset.kit})));
})();
