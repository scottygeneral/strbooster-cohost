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
