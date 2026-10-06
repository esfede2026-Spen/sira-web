document.addEventListener('DOMContentLoaded',()=>{const f=document.querySelector('#residencia-form');if(!f)return;const $=n=>document.querySelector('#id_'+n);const reset=n=>{const e=$(n);if(e)e.innerHTML='<option value="">Seleccione…</option>'};async function load(tipo,params,target,idk,nk){const e=$(target);reset(target);const clean=Object.fromEntries(Object.entries(params).filter(([,v])=>v));if(!Object.keys(clean).length)return;try{const r=await fetch(`${f.dataset.geoUrl}${tipo}/?${new URLSearchParams(clean)}`);if(!r.ok)throw new Error();const data=await r.json();data.forEach(x=>e.add(new Option(x[nk],x[idk])))}catch{console.error('No se pudo cargar '+tipo)}}
$('paisId')?.addEventListener('change',e=>{['estadoId','ciudadId','municipioId','parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('estados',{paisId:e.target.value},'estadoId','id_estado','desc_estado')});
$('estadoId')?.addEventListener('change',e=>{['ciudadId','municipioId','parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('ciudades',{estadoId:e.target.value},'ciudadId','id_ciudad','desc_ciudad');load('municipios',{estadoId:e.target.value},'municipioId','id_municipio','desc_municipio')});
$('ciudadId')?.addEventListener('change',e=>{['municipioId','parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('municipios',{ciudadId:e.target.value,estadoId:$('estadoId')?.value},'municipioId','id_municipio','desc_municipio')});
$('municipioId')?.addEventListener('change',e=>{['parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('parroquias',{municipioId:e.target.value},'parroquiaId','id_parroquia','desc_parroquia')});
const sectors=()=>load('sectores',{estadoId:$('estadoId')?.value,ciudadId:$('ciudadId')?.value,municipioId:$('municipioId')?.value,parroquiaId:$('parroquiaId')?.value,tipoSectorId:$('tipoSectorId')?.value},'sectorId','id_sector_geografico','desc_sector_geografico');$('parroquiaId')?.addEventListener('change',sectors);$('tipoSectorId')?.addEventListener('change',sectors);$('sectorId')?.addEventListener('change',e=>load('codigos-postales',{sectorId:e.target.value},'codigoPostalId','id_codigo_postal','codigo_postal'));});


/* CDC SIRA Responsive V2: navegación, tarjetas y barra móvil. */
document.addEventListener('DOMContentLoaded',()=>{
 const body=document.body, toggle=document.querySelector('.menu-toggle'), nav=document.querySelector('#sira-nav');
 const setMenu=open=>{body.classList.toggle('menu-open',open);toggle?.setAttribute('aria-expanded',String(open));};
 toggle?.addEventListener('click',()=>setMenu(true));
 document.querySelector('.menu-close')?.addEventListener('click',()=>setMenu(false));
 document.querySelector('.nav-overlay')?.addEventListener('click',()=>setMenu(false));
 nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
 document.querySelectorAll('.nav-submenu').forEach(b=>b.addEventListener('click',()=>{const open=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',String(open));b.closest('.nav-group')?.classList.toggle('submenu-open',open);}));
 document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
 document.querySelectorAll('.table table').forEach(table=>{const heads=[...table.querySelectorAll('thead th')].map(x=>x.textContent.trim());table.querySelectorAll('tbody tr').forEach(row=>[...row.children].forEach((cell,i)=>cell.dataset.label=heads[i]||''));});
 document.querySelector('[data-action="back"]')?.addEventListener('click',()=>history.back());
 const save=document.querySelector('[data-action="save"]');
 const forms=[...document.querySelectorAll('main form')].filter(f=>getComputedStyle(f).display!=='none');
 const primary=forms.find(f=>f.querySelector('.primary'))||forms[0];
 if(!primary){save?.setAttribute('disabled','');save?.classList.add('is-disabled');}
 save?.addEventListener('click',()=>primary?.requestSubmit());
});
