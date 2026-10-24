document.addEventListener('DOMContentLoaded',()=>{
 const f=document.querySelector('#residencia-form');
 if(!f)return;
 const $=n=>document.querySelector('#id_'+n);
 const reset=n=>{const e=$(n);if(e)e.innerHTML='<option value="">Seleccione…</option>'};
 async function load(tipo,params,target,idk,nk){
  const e=$(target);reset(target);if(!e)return;
  const clean=Object.fromEntries(Object.entries(params).filter(([,v])=>v));
  if(tipo!=='tipos-sector'&&!Object.keys(clean).length)return;
  try{
   const r=await fetch(`${f.dataset.geoUrl}${tipo}/?${new URLSearchParams(clean)}`);
   if(!r.ok)throw new Error();
   const data=await r.json();data.forEach(x=>e.add(new Option(x[nk],x[idk])));
  }catch{console.error('No se pudo cargar '+tipo)}
 }
 if($('tipoSectorId')&&$('tipoSectorId').options.length<=1)load('tipos-sector',{},'tipoSectorId','id_tipo_sector_geografico','desc_tipo_sector_geografico');
 if($('paisId')?.value&&$('estadoId')?.options.length<=1)load('estados',{paisId:$('paisId').value},'estadoId','id_estado','desc_estado');
 if($('estadoId')?.value&&$('ciudadId')?.options.length<=1)load('ciudades',{estadoId:$('estadoId').value},'ciudadId','id_ciudad','desc_ciudad');
 if($('ciudadId')?.value&&$('municipioId')?.options.length<=1)load('municipios',{ciudadId:$('ciudadId').value},'municipioId','id_municipio','desc_municipio');
 if($('municipioId')?.value&&$('parroquiaId')?.options.length<=1)load('parroquias',{municipioId:$('municipioId').value},'parroquiaId','id_parroquia','desc_parroquia');
 $('paisId')?.addEventListener('change',e=>{['estadoId','ciudadId','municipioId','parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('estados',{paisId:e.target.value},'estadoId','id_estado','desc_estado')});
 $('estadoId')?.addEventListener('change',e=>{['ciudadId','municipioId','parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('ciudades',{estadoId:e.target.value},'ciudadId','id_ciudad','desc_ciudad')});
 $('ciudadId')?.addEventListener('change',e=>{['municipioId','parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('municipios',{ciudadId:e.target.value},'municipioId','id_municipio','desc_municipio')});
 $('municipioId')?.addEventListener('change',e=>{['parroquiaId','sectorId','codigoPostalId'].forEach(reset);load('parroquias',{municipioId:e.target.value},'parroquiaId','id_parroquia','desc_parroquia')});
 const sectors=()=>{['sectorId','codigoPostalId'].forEach(reset);load('sectores',{estadoId:$('estadoId')?.value,ciudadId:$('ciudadId')?.value,municipioId:$('municipioId')?.value,parroquiaId:$('parroquiaId')?.value,tipoSectorId:$('tipoSectorId')?.value},'sectorId','id_sector_geografico','desc_sector_geografico')};
 $('parroquiaId')?.addEventListener('change',sectors);$('tipoSectorId')?.addEventListener('change',sectors);
 $('sectorId')?.addEventListener('change',e=>load('codigos-postales',{sectorId:e.target.value},'codigoPostalId','id_codigo_postal','codigo_postal'));
});

document.addEventListener('DOMContentLoaded',()=>{
 const body=document.body,toggle=document.querySelector('.menu-toggle'),nav=document.querySelector('#sira-nav');
 const setMenu=open=>{body.classList.toggle('menu-open',open);toggle?.setAttribute('aria-expanded',String(open));};
 toggle?.addEventListener('click',()=>setMenu(true));document.querySelector('.menu-close')?.addEventListener('click',()=>setMenu(false));document.querySelector('.nav-overlay')?.addEventListener('click',()=>setMenu(false));nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
 document.querySelectorAll('.table table').forEach(table=>{const heads=[...table.querySelectorAll('thead th')].map(x=>x.textContent.trim());table.querySelectorAll('tbody tr').forEach(row=>[...row.children].forEach((cell,i)=>cell.dataset.label=heads[i]||''));});
 document.querySelector('[data-action="back"]')?.addEventListener('click',()=>history.back());
 const save=document.querySelector('[data-action="save"]'),forms=[...document.querySelectorAll('main form')].filter(f=>getComputedStyle(f).display!=='none'),primary=forms.find(f=>f.querySelector('.primary'))||forms[0];if(!primary){save?.setAttribute('disabled','');save?.classList.add('is-disabled');}save?.addEventListener('click',()=>primary?.requestSubmit());
});
// ============================================================================
// Teléfono Compuesto: Código de País, Código de Área dinámico y Teléfono
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  const VENEZUELA_MOBILES = [
    { code: '414', desc: 'Movistar' },
    { code: '424', desc: 'Movistar' },
    { code: '412', desc: 'Digitel' },
    { code: '422', desc: 'Digitel' },
    { code: '416', desc: 'Movilnet' },
    { code: '426', desc: 'Movilnet' }
  ];

  const VENEZUELA_FIXED = [
    { code: '212', desc: 'Gran Caracas / Miranda / Vargas' },
    { code: '234', desc: 'Miranda (Barlovento)' },
    { code: '235', desc: 'Guárico' },
    { code: '238', desc: 'Guárico' },
    { code: '239', desc: 'Miranda (Valles del Tuy)' },
    { code: '240', desc: 'Barinas' },
    { code: '241', desc: 'Carabobo (Valencia)' },
    { code: '242', desc: 'Carabobo (Puerto Cabello)' },
    { code: '243', desc: 'Aragua (Maracay)' },
    { code: '244', desc: 'Aragua (La Victoria / Cagua)' },
    { code: '245', desc: 'Carabobo (Guacara)' },
    { code: '246', desc: 'Guárico' },
    { code: '247', desc: 'Apure' },
    { code: '248', desc: 'Amazonas' },
    { code: '249', desc: 'Carabobo' },
    { code: '251', desc: 'Lara (Barquisimeto)' },
    { code: '252', desc: 'Lara (Carora)' },
    { code: '253', desc: 'Lara' },
    { code: '254', desc: 'Yaracuy (San Felipe)' },
    { code: '255', desc: 'Portuguesa (Acarigua / Araure)' },
    { code: '256', desc: 'Portuguesa' },
    { code: '257', desc: 'Portuguesa (Guanare)' },
    { code: '258', desc: 'Cojedes (San Carlos)' },
    { code: '259', desc: 'Falcón' },
    { code: '261', desc: 'Zulia (Maracaibo)' },
    { code: '262', desc: 'Zulia (Cabimas)' },
    { code: '263', desc: 'Zulia' },
    { code: '264', desc: 'Zulia (Ciudad Ojeda)' },
    { code: '265', desc: 'Zulia' },
    { code: '266', desc: 'Zulia' },
    { code: '267', desc: 'Zulia' },
    { code: '268', desc: 'Falcón (Coro)' },
    { code: '269', desc: 'Falcón (Punto Fijo)' },
    { code: '271', desc: 'Zulia (Sur del Lago)' },
    { code: '272', desc: 'Barinas' },
    { code: '273', desc: 'Barinas' },
    { code: '274', desc: 'Mérida' },
    { code: '275', desc: 'Mérida (El Vigía)' },
    { code: '276', desc: 'Táchira (San Cristóbal)' },
    { code: '277', desc: 'Táchira' },
    { code: '278', desc: 'Apure' },
    { code: '281', desc: 'Anzoátegui (Pto. La Cruz / Barcelona)' },
    { code: '282', desc: 'Anzoátegui (Anaco / Cantaura)' },
    { code: '283', desc: 'Anzoátegui (El Tigre)' },
    { code: '284', desc: 'Bolívar' },
    { code: '285', desc: 'Bolívar (Ciudad Bolívar)' },
    { code: '286', desc: 'Bolívar (Puerto Ordaz / San Félix)' },
    { code: '287', desc: 'Delta Amacuro' },
    { code: '288', desc: 'Bolívar (Guasipati / Tumeremo)' },
    { code: '289', desc: 'Bolívar (Santa Elena de Uairén)' },
    { code: '291', desc: 'Monagas (Maturín)' },
    { code: '292', desc: 'Monagas (Caripito)' },
    { code: '293', desc: 'Sucre (Cumaná)' },
    { code: '294', desc: 'Sucre (Carúpano)' },
    { code: '295', desc: 'Nueva Esparta (Margarita)' }
  ];

  let catalogExtra = [];
  try {
    const rawData = document.getElementById('sira-codigos-catalogo')?.textContent;
    if (rawData) {
      const parsed = JSON.parse(rawData);
      if (Array.isArray(parsed)) {
        catalogExtra = parsed
          .filter(x => (x.codigo_pais === '+58' || !x.codigo_pais) && x.codigo_area_operador)
          .map(x => ({
            code: (x.codigo_area_sin_cero || x.codigo_area_operador.replace(/^0+/, '')),
            desc: x.descripcion || (x.tipo_linea === 'CELULAR' ? 'Móvil' : 'Nacional')
          }));
      }
    }
  } catch (e) {
    console.warn('No se pudo parsear el catálogo telefónico extra', e);
  }

  const veAllMap = new Map();
  [...VENEZUELA_MOBILES, ...VENEZUELA_FIXED, ...catalogExtra].forEach(item => {
    if (item && item.code && !veAllMap.has(item.code)) {
      veAllMap.set(item.code, item);
    }
  });
  const ALL_VE_CODES = Array.from(veAllMap.values());

  document.querySelectorAll('input[name="codigoArea"]').forEach(areaInput => {
    const form = areaInput.closest('form') || document;
    const paisSelect = form.querySelector('select[name="codigoPais"]') || areaInput.parentElement.querySelector('select[name="codigoPais"]');
    const numInput = form.querySelector('input[name="numero"]');
    const datalistId = areaInput.getAttribute('list');
    let datalist = datalistId ? document.getElementById(datalistId) : null;

    if (!datalist) {
      const newId = 'datalist_area_' + Math.random().toString(36).substring(2, 8);
      datalist = document.createElement('datalist');
      datalist.id = newId;
      document.body.appendChild(datalist);
      areaInput.setAttribute('list', newId);
    }

    const renderOptions = (items) => {
      datalist.innerHTML = items
        .map(i => '<option value="' + i.code + '"></option>')
        .join('');
    };

    const updateCountryState = () => {
      const isVe = !paisSelect || paisSelect.value === '+58' || paisSelect.value === '';
      if (isVe) {
        areaInput.placeholder = '412';
        areaInput.maxLength = 5;
        if (numInput) {
          numInput.placeholder = '1234567';
          numInput.maxLength = 7;
        }
        const currentVal = areaInput.value.trim().replace(/^0+/, '');
        if (!currentVal) {
          renderOptions(VENEZUELA_MOBILES);
        } else {
          filterVeCodes(currentVal);
        }
      } else {
        areaInput.placeholder = 'Área';
        areaInput.maxLength = 6;
        if (numInput) {
          numInput.placeholder = 'Número';
          numInput.maxLength = 15;
        }
        renderOptions([]);
      }
    };

    const filterVeCodes = (val) => {
      const clean = val.replace(/^0+/, '').replace(/\D/g, '');
      if (!clean) {
        renderOptions(VENEZUELA_MOBILES);
        return;
      }
      const matches = ALL_VE_CODES.filter(x => x.code.startsWith(clean) || x.code.includes(clean));
      renderOptions(matches.length > 0 ? matches.slice(0, 15) : []);
    };

    areaInput.addEventListener('focus', () => {
      const isVe = !paisSelect || paisSelect.value === '+58' || paisSelect.value === '';
      if (isVe) {
        const val = areaInput.value.trim().replace(/^0+/, '');
        if (!val) {
          renderOptions(VENEZUELA_MOBILES);
        } else {
          filterVeCodes(val);
        }
      }
    });

    areaInput.addEventListener('input', (e) => {
      let val = e.target.value;
      val = val.replace(/^0+/, '').replace(/\D/g, '');
      if (e.target.value !== val) {
        e.target.value = val;
      }
      const isVe = !paisSelect || paisSelect.value === '+58' || paisSelect.value === '';
      if (isVe) {
        filterVeCodes(val);
      }
    });

    if (numInput) {
      numInput.addEventListener('input', (e) => {
        let val = e.target.value.replace(/\D/g, '');
        const isVe = !paisSelect || paisSelect.value === '+58' || paisSelect.value === '';
        if (isVe && val.length > 7) {
          val = val.slice(0, 7);
        } else if (!isVe && val.length > 15) {
          val = val.slice(0, 15);
        }
        if (e.target.value !== val) {
          e.target.value = val;
        }
      });
    }

    if (paisSelect) {
      paisSelect.addEventListener('change', updateCountryState);
    }

    updateCountryState();
  });
});

// ============================================================================
// Menú Subnavegación Personas: Soporte Click & Hover Seguro
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-submenu').forEach(b => {
    b.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const group = b.closest('.nav-group');
      const isAlreadyOpen = group?.classList.contains('submenu-open');
      document.querySelectorAll('.nav-group.submenu-open').forEach(g => {
        g.classList.remove('submenu-open');
        g.querySelector('.nav-submenu')?.setAttribute('aria-expanded', 'false');
      });
      if (!isAlreadyOpen && group) {
        group.classList.add('submenu-open');
        b.setAttribute('aria-expanded', 'true');
      }
    });
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-group')) {
      document.querySelectorAll('.nav-group.submenu-open').forEach(g => {
        g.classList.remove('submenu-open');
        g.querySelector('.nav-submenu')?.setAttribute('aria-expanded', 'false');
      });
    }
  });
});

// ============================================================================
// Formato de Fecha en Español: DD/MM/AAAA con Máscara y Selector de Calendario
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.field-fecha-nac').forEach(input => {
    input.setAttribute('placeholder', 'DD/MM/AAAA');
    input.setAttribute('maxlength', '10');

    input.addEventListener('input', (e) => {
      let v = e.target.value.replace(/\D/g, '');
      if (v.length > 8) v = v.slice(0, 8);
      let formatted = '';
      if (v.length > 4) {
        formatted = `${v.slice(0, 2)}/${v.slice(2, 4)}/${v.slice(4)}`;
      } else if (v.length > 2) {
        formatted = `${v.slice(0, 2)}/${v.slice(2)}`;
      } else {
        formatted = v;
      }
      e.target.value = formatted;
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace') {
        const val = input.value;
        if (val.endsWith('/')) {
          e.preventDefault();
          input.value = val.slice(0, -1);
        }
      }
    });
  });
});

window.abrirCalendarioFecha = function(inputId, triggerBtn) {
  const textInput = document.getElementById(inputId);
  if (!textInput) return;
  let helper = document.getElementById('calendar_picker_helper');
  if (!helper) {
    helper = document.createElement('input');
    helper.type = 'date';
    helper.id = 'calendar_picker_helper';
    document.body.appendChild(helper);
  }

  const btn = triggerBtn || (typeof event !== 'undefined' && event?.target ? event.target.closest('button') : null) || textInput.parentElement?.querySelector('button');
  if (btn) {
    const rect = btn.getBoundingClientRect();
    helper.style.position = 'fixed';
    helper.style.top = Math.max(0, rect.top) + 'px';
    helper.style.left = Math.max(0, rect.left) + 'px';
    helper.style.width = Math.max(20, rect.width) + 'px';
    helper.style.height = Math.max(20, rect.height) + 'px';
    helper.style.opacity = '0.01';
    helper.style.pointerEvents = 'none';
    helper.style.zIndex = '99999';
  } else {
    helper.style.position = 'fixed';
    helper.style.opacity = '0.01';
    helper.style.pointerEvents = 'none';
    helper.style.top = '100px';
    helper.style.left = '100px';
  }

  // Si ya tiene valor (DD/MM/AAAA o YYYY-MM-DD o timestamp), sincronizarlo al date input
  let raw = (textInput.value || '').trim().split('T')[0].split(' ')[0];
  if (raw.includes('-')) {
    const p = raw.split('-');
    if (p.length === 3 && p[0].length === 4) {
      helper.value = `${p[0]}-${p[1].padStart(2, '0')}-${p[2].padStart(2, '0')}`;
      textInput.value = `${p[2].padStart(2, '0')}/${p[1].padStart(2, '0')}/${p[0]}`;
    }
  } else if (raw.includes('/')) {
    const parts = raw.split('/');
    if (parts.length === 3 && parts[2].length === 4) {
      helper.value = `${parts[2]}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}`;
    }
  }

  helper.onchange = function() {
    if (helper.value) {
      const dp = helper.value.split('-');
      if (dp.length === 3) {
        textInput.value = `${dp[2]}/${dp[1]}/${dp[0]}`;
        textInput.dispatchEvent(new Event('input', { bubbles: true }));
        textInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
  };

  if (typeof helper.showPicker === 'function') {
    try {
      helper.showPicker();
    } catch {
      helper.click();
    }
  } else {
    helper.click();
  }
};

