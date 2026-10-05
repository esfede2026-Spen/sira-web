document.addEventListener('DOMContentLoaded',()=>{
 const toggle=document.querySelector('.nav-toggle'); const nav=document.querySelector('.main-nav');
 if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});}
 document.querySelectorAll('.nav-trigger').forEach(btn=>btn.addEventListener('click',e=>{e.stopPropagation();const box=btn.parentElement;document.querySelectorAll('.nav-dropdown.open').forEach(x=>{if(x!==box)x.classList.remove('open');});const open=box.classList.toggle('open');btn.setAttribute('aria-expanded',String(open));}));
 document.addEventListener('click',()=>document.querySelectorAll('.nav-dropdown.open').forEach(x=>x.classList.remove('open')));
});
