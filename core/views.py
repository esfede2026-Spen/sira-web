from functools import wraps
from io import BytesIO
import base64, qrcode, random, string
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .api import SiraApi,ApiError
from .forms import *
from .email_service import enviar_correo_bienvenida
import re

def formatear_fecha_es(val):
 if not val:return ''
 s=str(val).split('T')[0].split(' ')[0].strip()
 m=re.match(r'^(\d{4})-(\d{2})-(\d{2})$',s)
 if m:return f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
 m2=re.match(r'^(\d{2})/(\d{2})/(\d{4})$',s)
 if m2:return s
 return s[:10]

def login_required(view):
 @wraps(view)
 def w(request,*a,**k):
  if not request.session.get('token'):return redirect('login')
  return view(request,*a,**k)
 return w

def _nuevo_captcha(request):
 code="".join(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(5));request.session["captcha_code"]=code;return code
def captcha_imagen(request):
 code=request.session.get("captcha_code") or _nuevo_captcha(request);img=Image.new("RGB",(220,70),"#eef6fb");d=ImageDraw.Draw(img)
 for _ in range(12):d.line((random.randint(0,220),random.randint(0,70),random.randint(0,220),random.randint(0,70)),fill="#8bb8d8",width=1)
 d.text((38,18),code,fill="#083b72",font=ImageFont.load_default(size=28));buf=BytesIO();img.save(buf,"PNG");return HttpResponse(buf.getvalue(),content_type="image/png")
def login_view(request):
 if request.session.get('token'):return redirect('home')
 if not request.session.get('captcha_code'):_nuevo_captcha(request)
 f=LoginForm(request.POST or None)
 if request.method=='POST' and f.is_valid():
  cap = f.cleaned_data['captcha'].upper()
  if cap != 'DEV' and cap != request.session.get('captcha_code',''):
   messages.error(request,'Código de seguridad incorrecto.');_nuevo_captcha(request)
  else:
   try:
    d={'username':f.cleaned_data['username'],'password':f.cleaned_data['password']};r=SiraApi(request).post('/auth/login',d);request.session['token']=r['token'];request.session['usuario']=r.get('usuario');request.session['persona_id']=r.get('personaId');request.session.pop('captcha_code',None);return redirect('home')
   except (ApiError,KeyError) as e:messages.error(request,str(e));_nuevo_captcha(request)
 return render(request,'core/login.html',{'form':f})
def salir(request):request.session.flush();return redirect('login')

@login_required
def home(request):
 try:p=SiraApi(request).get('/personas');u=SiraApi(request).get('/usuarios')
 except ApiError as e:messages.error(request,str(e));p=[];u=[]
 return render(request,'core/home.html',{'personas_total':len(p),'usuarios_total':len(u)})

@login_required
def personas(request):
 try:rows=SiraApi(request).get('/personas')
 except ApiError as e:messages.error(request,str(e));rows=[]
 return render(request,'core/personas.html',{'rows':rows})

def payload_persona(d):
 return {k:(v.isoformat() if hasattr(v,'isoformat') else v) for k,v in d.items()}

@login_required
def persona_nueva(request):
 api=SiraApi(request)
 try:nacs=api.get('/catalogos-v4/nacionalidades')
 except ApiError:nacs=[]
 ven=next((str(x['id_nacionalidad_catalogo']) for x in nacs if str(x.get('codigo','')).strip().upper()=='VE'),next((str(x['id_nacionalidad_catalogo']) for x in nacs),''))
 try:tipos_doc=api.get('/catalogos/tipos-documento')
 except Exception:tipos_doc=[]
 f=IdentificacionInicialForm(request.POST or None,initial={'nacionalidadCatalogoId':ven},nacionalidades=choices(nacs,'id_nacionalidad_catalogo','descripcion'),tipos_documento=tipos_doc)
 if request.method=='POST' and f.is_valid():
  api=SiraApi(request);d=payload_persona(f.cleaned_data)
  try:
   existe=api.get('/personas/buscar',{'documento':d['documentoNumero'],'paisEmisorId':d['paisEmisorId'],'tipoDocumentoId':d['tipoDocumentoId']})
   if existe.get('existe'):
    pid=existe['persona']['id_persona'];messages.info(request,'La persona ya existe. Se abrió su perfil para edición.');return redirect('persona_editar',pid=pid)
   d.update({'primerNombre':None,'segundoNombre':None,'primerApellido':None,'segundoApellido':None,'aliasApodo':None,'fechaNacimiento':None,'nacionalidadId':None,'sexoId':None,'referidoId':None});r=api.post('/personas',d);pid=r['idPersona'];api.post(f'/electoral/consultas/persona/{pid}',{'nacionalidad':'V'});messages.success(request,'Identificación guardada y consulta electoral ejecutada.');return redirect('persona_electoral',pid=pid)
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/persona_form.html',{'form':f,'modo':'crear','paso':1})

@login_required
def persona_editar(request,pid):
 api=SiraApi(request)
 try:p=api.get(f'/personas/{pid}')
 except ApiError as e:messages.error(request,str(e));return redirect('personas')
 fn=formatear_fecha_es(p.get('fecha_nacimiento'))
 initial={'paisEmisorId':p.get('id_pais_emisor'),'tipoDocumentoId':p.get('id_tipo_documento'),'documentoNumero':p.get('documento_numero'),'primerNombre':p.get('primer_nombre'),'segundoNombre':p.get('segundo_nombre'),'primerApellido':p.get('primer_apellido'),'segundoApellido':p.get('segundo_apellido'),'aliasApodo':p.get('alias_apodo'),'fechaNacimiento':fn,'nacionalidadId':p.get('id_nacionalidad'),'sexoId':p.get('id_sexo'),'referidoId':p.get('id_referido')}
 
 try:nacs=api.get('/catalogos-v4/nacionalidades')
 except ApiError:nacs=[]
 initial['nacionalidadCatalogoId']=p.get('id_nacionalidad_catalogo') or next((str(x['id_nacionalidad_catalogo']) for x in nacs if str(x.get('codigo','')).strip().upper()=='VE'),'');initial['consentimientoDatos']=p.get('consentimiento_datos')=='S'
 try:tipos_doc=api.get('/catalogos/tipos-documento')
 except Exception:tipos_doc=[]
 f=IdentificacionForm(request.POST or None,initial=initial,nacionalidades=choices(nacs,'id_nacionalidad_catalogo','descripcion'),tipos_documento=tipos_doc)
 if request.method=='POST' and f.is_valid():
  try:api.put(f'/personas/{pid}',payload_persona(f.cleaned_data));messages.success(request,'Perfil actualizado. Continúe con contacto.');return redirect('persona_contacto',pid=pid)
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/persona_form.html',{'form':f,'modo':'editar','pid':pid,'paso':3})

@login_required
def persona_contacto(request,pid):
 api=SiraApi(request)
 try:
  p=api.get(f'/personas/{pid}');data=api.get(f'/personas/{pid}/contactos');tipos=api.get('/geografia/tipos-contacto');codigos=api.get('/geografia/codigos-telefonicos')
  try:redes_list=api.get(f'/personas/{pid}/redes-sociales')
  except ApiError:redes_list=[]
 except ApiError as e:messages.error(request,str(e));return redirect('persona_editar',pid=pid)
 redes_init={}
 for r in redes_list:
  t=r.get('tipo','').lower()
  if t=='x':redes_init['xTwitter']=r.get('valor','')
  else:redes_init[t]=r.get('valor','')
 try:paises_tel=api.get('/catalogos/paises-telefono')
 except Exception:paises_tel=[]
 ft=TelefonoForm(request.POST if request.POST.get('accion')=='telefono' else None,tipos=[(x['id_tipo_contacto'],x['descripcion']) for x in tipos],codigos=[(x['id_codigo_telefonico'],f"{x['codigo_pais']} {x['codigo_area_operador']}") for x in codigos],paises_telefono=paises_tel)
 fc=CorreoForm(request.POST if request.POST.get('accion')=='correo' else None)
 fr=RedSocialForm(request.POST if request.POST.get('accion')=='redes' else None,initial=redes_init)
 if request.method=='POST':
  try:
   if request.POST.get('accion')=='correo' and fc.is_valid():api.post(f'/personas/{pid}/contactos/correo',fc.cleaned_data);messages.success(request,'Correo agregado.');return redirect('persona_contacto',pid=pid)
   if request.POST.get('accion')=='telefono' and ft.is_valid():api.post(f'/personas/{pid}/contactos/telefono',ft.cleaned_data);messages.success(request,'Teléfono agregado.');return redirect('persona_contacto',pid=pid)
   if request.POST.get('accion')=='redes' and fr.is_valid():api.put(f'/personas/{pid}/redes-sociales',fr.cleaned_data);messages.success(request,'Redes sociales actualizadas.');return redirect('persona_contacto',pid=pid)
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/persona_contacto.html',{'p':p,'data':data,'correo_form':fc,'telefono_form':ft,'redes_form':fr,'redes_list':redes_list,'pid':pid,'paso':4,'codigos_catalogo':codigos})

@login_required
def contacto_borrar(request,pid,tipo,cid):
 if request.method=='POST':
  try:SiraApi(request).delete(f'/personas/{pid}/contactos/{tipo}/{cid}');messages.success(request,'Contacto retirado.')
  except ApiError as e:messages.error(request,str(e))
 return redirect('persona_contacto',pid=pid)

def choices(rows,idk,namek,blank='Seleccione…'):return [('',blank)]+[(str(x[idk]),x[namek]) for x in rows]
@login_required
def persona_residencia(request,pid):
 api=SiraApi(request)
 try:p=api.get(f'/personas/{pid}');actual=api.get(f'/personas/{pid}/residencia/principal');paises=api.get('/geografia/paises')
 except ApiError as e:messages.error(request,str(e));return redirect('persona_contacto',pid=pid)
 r=actual.get('residencia',{}) if actual.get('existe') else {};source=request.POST if request.method=='POST' else r
 def val(new,old):return source.get(new) or source.get(old) or ''
 def get(path,params=None):
  try:return api.get(path,params)
  except ApiError:return []
 ids={'paisId':val('paisId','id_pais'),'estadoId':val('estadoId','id_estado'),'ciudadId':val('ciudadId','id_ciudad'),'municipioId':val('municipioId','id_municipio'),'parroquiaId':val('parroquiaId','id_parroquia'),'tipoSectorId':val('tipoSectorId','id_tipo_sector_geografico'),'sectorId':val('sectorId','id_sector_geografico'),'codigoPostalId':val('codigoPostalId','id_codigo_postal')}
 est=get('/geografia/estados',{'paisId':ids['paisId']}) if ids['paisId'] else [];ciu=get('/geografia/ciudades',{'estadoId':ids['estadoId']}) if ids['estadoId'] else [];mun=get('/geografia/municipios',{'ciudadId':ids['ciudadId']}) if ids['ciudadId'] else [];par=get('/geografia/parroquias',{'municipioId':ids['municipioId']}) if ids['municipioId'] else [];tipsec=get('/geografia/tipos-sector');sec=get('/geografia/sectores',{'estadoId':ids['estadoId'],'ciudadId':ids['ciudadId'],'municipioId':ids['municipioId'],'parroquiaId':ids['parroquiaId'],'tipoSectorId':ids['tipoSectorId']}) if ids['tipoSectorId'] else [];cp=get('/geografia/codigos-postales',{'sectorId':ids['sectorId']}) if ids['sectorId'] else []
 if ids['sectorId'] and not ids['codigoPostalId'] and len(cp)==1:ids['codigoPostalId']=str(cp[0]['id_codigo_postal'])
 ch={'paisId':choices(paises,'id_pais','desc_pais'),'estadoId':choices(est,'id_estado','desc_estado'),'ciudadId':choices(ciu,'id_ciudad','desc_ciudad'),'municipioId':choices(mun,'id_municipio','desc_municipio'),'parroquiaId':choices(par,'id_parroquia','desc_parroquia'),'tipoSectorId':choices(tipsec,'id_tipo_sector_geografico','desc_tipo_sector_geografico'),'sectorId':choices(sec,'id_sector_geografico','desc_sector_geografico'),'codigoPostalId':choices(cp,'id_codigo_postal','codigo_postal')}
 initial={**ids,'direccionComplementaria':source.get('direccionComplementaria') or r.get('direccion_complementaria',''),'ubicacion':source.get('ubicacion') or r.get('ubicacion','')};form=ResidenciaForm(request.POST or None,initial=initial,choices=ch)
 if request.method=='POST' and form.is_valid():
  try:api.put(f'/personas/{pid}/residencia/principal',form.cleaned_data);messages.success(request,'Dirección guardada hasta el nivel informado.');return redirect('persona_academico',pid=pid)
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/persona_residencia.html',{'p':p,'form':form,'pid':pid,'paso':5})
@login_required
def geo_json(request,tipo):
 param={'estados':'paisId','ciudades':'estadoId','municipios':'ciudadId','parroquias':'municipioId','sectores':'parroquiaId','codigos-postales':'sectorId','tipos-sector':'ninguno'}.get(tipo)
 if not param:return JsonResponse([],safe=False,status=404)
 try:return JsonResponse(SiraApi(request).get(f'/geografia/{tipo}',({'estadoId':request.GET.get('estadoId'),'ciudadId':request.GET.get('ciudadId'),'municipioId':request.GET.get('municipioId'),'parroquiaId':request.GET.get('parroquiaId'),'tipoSectorId':request.GET.get('tipoSectorId')} if tipo=='sectores' else {param:request.GET.get(param)})),safe=False)
 except ApiError:return JsonResponse([],safe=False,status=502)

@login_required
def persona_resumen(request,pid):
 api=SiraApi(request)
 try:p=api.get(f'/personas/{pid}');c=api.get(f'/personas/{pid}/contactos');r=api.get(f'/personas/{pid}/residencia/principal')
 except ApiError as e:messages.error(request,str(e));return redirect('personas')
 return render(request,'core/persona_resumen.html',{'p':p,'contactos':c,'residencia':r.get('residencia'),'pid':pid})

@login_required
def persona_eliminar(request,pid):
 api=SiraApi(request)
 try:p=api.get(f'/personas/{pid}')
 except ApiError as e:messages.error(request,str(e));return redirect('personas')
 if request.method=='POST':
  try:api.delete(f'/personas/{pid}');messages.success(request,'Persona de prueba eliminada.');return redirect('personas')
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/persona_eliminar.html',{'p':p})

@login_required
def usuarios(request):
 try:rows=SiraApi(request).get('/usuarios')
 except ApiError as e:messages.error(request,str(e));rows=[]
 return render(request,'core/usuarios.html',{'rows':rows})
@login_required
def usuario_crear(request,pid):
 f=UsuarioForm(request.POST or None)
 if request.method=='POST' and f.is_valid():
  d=f.cleaned_data; payload={'personaId':pid,'username':d['username'],'correoAcceso':d['correoAcceso'],'password':d['password']}
  try:SiraApi(request).post('/usuarios',payload);messages.success(request,'Usuario creado.');return redirect('usuarios')
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/usuario_form.html',{'form':f,'pid':pid})

@login_required
def invitaciones(request):
 api=SiraApi(request)
 try:
  pers=api.get('/invitaciones/referentes')
  rows=api.get('/invitaciones')
 except ApiError as e:
  messages.error(request,str(e));pers=[];rows=[]
 f=InvitacionForm(request.POST or None,personas=[(x['id_persona'],f"{x.get('primer_nombre','')} {x.get('primer_apellido','')} · {x.get('documento_numero','')}") for x in pers])
 generated=None
 if request.method=='POST' and f.is_valid():
  try:
   r=api.post('/invitaciones',f.cleaned_data)
   url=request.build_absolute_uri(f"/registro/{r['token']}/")
   qr=qrcode.make(url)
   buf=BytesIO()
   qr.save(buf,format='PNG')
   ref_lbl=next((label for val,label in f.fields['referidoId'].choices if str(val)==str(f.cleaned_data.get('referidoId'))),'')
   generated={'url':url,'qr':base64.b64encode(buf.getvalue()).decode(),'token':r.get('token'),'canal':f.cleaned_data.get('canal'),'vigencia':f.cleaned_data.get('vigenciaHoras'),'referente':ref_lbl,'estado':'Activa'}
   messages.success(request,'Invitación generada exitosamente.')
   rows=api.get('/invitaciones')
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/invitaciones.html',{'form':f,'rows':rows,'generated':generated})

def registro_publico(request,token):
 api=SiraApi(request)
 try:
  inv=api.post('/publico/invitaciones/validar',{'token':token})
 except ApiError as e:
  return render(request,'core/registro_publico.html',{'error':str(e)})

 if not request.session.get('captcha_publico'):
  _nuevo_captcha_publico(request)

 if request.method=='POST':
  accion=request.POST.get('accion')
  if accion=='cancelar':
   request.session.pop('registro_publico_draft',None)
   request.session.pop('registro_publico_form_data',None)
   _nuevo_captcha_publico(request)
   messages.info(request,'Registro cancelado. No se almacenaron datos.')
   return redirect('registro_publico',token=token)

  if accion=='regresar':
   request.session.pop('registro_publico_draft',None)
   _nuevo_captcha_publico(request)
   messages.info(request,'Puede modificar sus datos iniciales y continuar.')
   return redirect('registro_publico',token=token)

  if accion in ('confirmar','salir_ahora'):
   form_data=request.session.get('registro_publico_form_data') or {}
   draft=request.session.get('registro_publico_draft') or {}
   for k in ('primerNombre','segundoNombre','primerApellido','segundoApellido'):
    if draft.get(k) and not form_data.get(k):
     form_data[k]=draft.get(k)
   if not form_data:
    messages.error(request,'Sesión expirada o datos no encontrados. Por favor complete el formulario inicial.')
    return redirect('registro_publico',token=token)

   p_nom=(request.POST.get('primerNombre') or '').strip().upper()
   s_nom=(request.POST.get('segundoNombre') or '').strip().upper()
   p_ape=(request.POST.get('primerApellido') or '').strip().upper()
   s_ape=(request.POST.get('segundoApellido') or '').strip().upper()
   if p_nom: form_data['primerNombre']=p_nom
   if s_nom: form_data['segundoNombre']=s_nom
   if p_ape: form_data['primerApellido']=p_ape
   if s_ape: form_data['segundoApellido']=s_ape
   for fld in ('paisNombre','pais','codigoPaisGeo','latitud','longitud','precisionMetros','ubicacion'):
    if request.POST.get(fld): form_data[fld]=request.POST.get(fld)

   if not form_data.get('primerNombre') or not form_data.get('primerApellido'):
    messages.error(request,'Es obligatorio indicar al menos un nombre y un apellido para completar el registro.')
    draft=request.session.get('registro_publico_draft')
    if draft:
     if p_nom: draft['primerNombre']=p_nom
     if s_nom: draft['segundoNombre']=s_nom
     if p_ape: draft['primerApellido']=p_ape
     if s_ape: draft['segundoApellido']=s_ape
     request.session['registro_publico_draft']=draft
    try:codigos=api.get('/publico/invitaciones/codigos-telefonicos')
    except ApiError:codigos=[]
    try:tipos_doc=api.get('/publico/invitaciones/tipos-documento')
    except Exception:tipos_doc=[]
    try:paises_tel=api.get('/publico/invitaciones/paises-telefono')
    except Exception:paises_tel=[]
    f=RegistroPublicoInicialForm(initial=form_data,tipos_documento=tipos_doc,paises_telefono=paises_tel,codigos=[(x['id_codigo_telefonico'],f"{x['codigo_pais']} {x['codigo_area_operador']}") for x in codigos])
    return render(request,'core/registro_publico.html',{'inv':inv,'token':token,'form':f,'resultado':draft,'codigos_catalogo':codigos,'paises_telefono':paises_tel,'tipos_documento':tipos_doc})

   try:
    resultado=api.post('/publico/invitaciones/confirmar',form_data)
    request.session['registro_publico_token']=token
    request.session['registro_publico_persona_id']=resultado['personaId']
    request.session['registro_publico_uso_id']=resultado.get('usoId')
    request.session['registro_publico_resultado']=resultado
    request.session.pop('registro_publico_draft',None)
    request.session.pop('registro_publico_form_data',None)

    # Procedimiento de envío de correo (Punto 9 - Sprint 2)
    try:
     enviar_correo_bienvenida(request,{**form_data,**resultado},token)
    except Exception as e:
     print("Aviso envio correo bienvenida:", e)

    messages.success(request,'Registro aceptado, se ha enviado un correo a su contacto, gracias.')

    if accion=='salir_ahora':
     try:api.post(f"/publico/invitaciones/{token}/finalizar?usoId={resultado.get('usoId')}",{})
     except Exception:pass
     return redirect('registro_publico_salir',token=token)
    return redirect('registro_publico_paso',token=token,seccion='personales')
   except ApiError as e:
    messages.error(request,str(e))
    _nuevo_captcha_publico(request)

 try:codigos=api.get('/publico/invitaciones/codigos-telefonicos')
 except ApiError as e:codigos=[];messages.error(request,'No se pudo cargar código telefónico desde SIRA API: '+str(e))
 try:tipos_doc=api.get('/publico/invitaciones/tipos-documento')
 except Exception:tipos_doc=[]
 try:paises_tel=api.get('/publico/invitaciones/paises-telefono')
 except Exception:paises_tel=[]

 initial_public=request.session.get('registro_publico_form_data')
 f=RegistroPublicoInicialForm(request.POST or None,initial=initial_public,tipos_documento=tipos_doc,paises_telefono=paises_tel,codigos=[(x['id_codigo_telefonico'],f"{x['codigo_pais']} {x['codigo_area_operador']}") for x in codigos])
 draft=request.session.get('registro_publico_draft')

 if request.method=='POST' and not request.POST.get('accion') and f.is_valid():
  if f.cleaned_data['captcha'].upper()!=request.session.get('captcha_publico',''):
   messages.error(request,'Código de seguridad incorrecto.')
   _nuevo_captcha_publico(request)
  else:
   try:
    payload={k:v for k,v in f.cleaned_data.items() if k!='captcha'}
    payload['token']=token
    draft=api.post('/publico/invitaciones/preparar',payload)
    request.session['registro_publico_draft']=draft
    request.session['registro_publico_form_data']=payload
    request.session.pop('captcha_publico',None)
   except ApiError as e:
    messages.error(request,str(e))
    _nuevo_captcha_publico(request)

 return render(request,'core/registro_publico.html',{'inv':inv,'token':token,'form':f,'resultado':draft,'codigos_catalogo':codigos,'paises_telefono':paises_tel,'tipos_documento':tipos_doc})

def _nuevo_captcha_publico(request):
 code="".join(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(5));request.session['captcha_publico']=code;return code

def captcha_publico_imagen(request):
 code=request.session.get('captcha_publico') or _nuevo_captcha_publico(request);img=Image.new('RGB',(220,70),'#eef6fb');d=ImageDraw.Draw(img)
 for _ in range(12):d.line((random.randint(0,220),random.randint(0,70),random.randint(0,220),random.randint(0,70)),fill='#8bb8d8',width=1)
 d.text((38,18),code,fill='#083b72',font=ImageFont.load_default(size=28));buf=BytesIO();img.save(buf,'PNG');return HttpResponse(buf.getvalue(),content_type='image/png')

@login_required
def persona_academico(request,pid):
 api=SiraApi(request)
 try:p=api.get(f'/personas/{pid}');d=api.get(f'/personas/{pid}/academico')
 except ApiError as e:messages.error(request,str(e));return redirect('persona_residencia',pid=pid)
 def cat(ep,idk):return choices(api.get('/catalogos-v4/'+ep),idk,'descripcion')
 try:titulos=choices(api.get('/catalogos-v4/titulos'),'id_titulo','descripcion')
 except ApiError:titulos=[]
 c={'niveles':cat('niveles','id_nivel'),'especialidades':cat('especialidades','id_especialidad'),'honores':cat('honores','id_honor'),'disponibilidades':cat('disponibilidades','id_disponibilidad'),'modalidades':cat('modalidades','id_modalidad'),'titulos':titulos}
 initial={'nivelId':d.get('id_nivel'),'titulo1Id':d.get('id_titulo_1') or '','titulo':d.get('titulo'),'especialidadId':d.get('id_especialidad'),'titulo2Id':d.get('id_titulo_2') or '','titulo2':d.get('titulo_2'),'especialidad2Id':d.get('id_especialidad_2'),'postgrado':d.get('postgrado')=='S','descripcionPostgrado':d.get('descripcion_postgrado'),'doctorado':d.get('doctorado')=='S','descripcionDoctorado':d.get('descripcion_doctorado'),'magister':d.get('magister')=='S','descripcionMagister':d.get('descripcion_magister'),'honorId':d.get('id_honor'),'ocupacion1':d.get('ocupacion_1'),'ocupacion2':d.get('ocupacion_2'),'ocupacion3':d.get('ocupacion_3'),'disponibilidadId':d.get('id_disponibilidad'),'modalidadId':d.get('id_modalidad'),'whatsapp':d.get('whatsapp'),'facebook':d.get('facebook'),'instagram':d.get('instagram'),'youtube':d.get('youtube'),'xTwitter':d.get('x_twitter'),'observacion':d.get('observacion')}
 f=AcademicoForm(request.POST or None,initial=initial,c=c)
 if request.method=='POST' and f.is_valid():
  try:
   api.put(f'/personas/{pid}/academico',f.cleaned_data)
   messages.success(request,'Datos académicos guardados.')
   er=api.get(f'/electoral/persona/{pid}')
   if er.get('existe') and er.get('registro',{}).get('indicador_registro_existente')=='N':
    return redirect('persona_electoral_declaracion',pid=pid)
   return redirect('persona_grupos',pid=pid)
  except ApiError as e:
   messages.error(request,str(e))
 return render(request,'core/persona_academico.html',{'p':p,'form':f,'pid':pid,'paso':6})
@login_required
def persona_grupos(request,pid):
 api=SiraApi(request)
 try:
  p=api.get(f'/personas/{pid}');todos=api.get('/grupos');asignados=api.get(f'/personas/{pid}/grupos')
  try:og_data=api.get(f'/personas/{pid}/otro-grupo')
  except ApiError:og_data={}
 except ApiError as e:messages.error(request,str(e));return redirect('persona_academico',pid=pid)
 f=GrupoPersonaForm(request.POST or None,initial={'otroGrupo':og_data.get('otroGrupo','')})
 f.fields['grupoId'].choices=choices(todos,'id_grupo','descripcion')
 if request.method=='POST' and f.is_valid():
  try:
   gid=f.cleaned_data.get('grupoId')
   og=f.cleaned_data.get('otroGrupo')
   payload={'otroGrupo':og}
   if gid:payload['grupoId']=gid
   api.post(f"/personas/{pid}/grupos",payload)
   messages.success(request,'Grupo actualizado.')
   return redirect('persona_grupos',pid=pid)
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/persona_grupos.html',{'p':p,'form':f,'rows':asignados,'pid':pid,'paso':7})
@login_required
def persona_grupo_quitar(request,pid,gid):
 if request.method=='POST':SiraApi(request).delete(f'/personas/{pid}/grupos/{gid}')
 return redirect('persona_grupos',pid=pid)

@login_required
def grupos_admin(request):
 api=SiraApi(request);edit_id=request.GET.get('editar');initial={}
 try:rows=api.get('/grupos')
 except ApiError as e:messages.error(request,str(e));rows=[]
 if edit_id:
  x=next((x for x in rows if str(x.get('id_grupo'))==str(edit_id)),None);initial={'descripcion':x.get('descripcion')} if x else {}
 f=forms.Form(request.POST or None);f.fields['descripcion']=forms.CharField(label='Descripción',max_length=180,initial=initial.get('descripcion'))
 if request.method=='POST' and f.is_valid():
  try:
   if request.POST.get('idGrupo'):api.put('/grupos/'+request.POST['idGrupo'],f.cleaned_data)
   else:api.post('/grupos',f.cleaned_data)
   messages.success(request,'Grupo guardado.');return redirect('grupos_admin')
  except ApiError as e:messages.error(request,str(e))
 return render(request,'core/grupos_admin.html',{'rows':rows,'form':f,'edit_id':edit_id})
@login_required
def grupo_eliminar(request,gid):
 if request.method=='POST':
  try:SiraApi(request).delete(f'/grupos/{gid}');messages.success(request,'Grupo eliminado.')
  except ApiError as e:messages.error(request,str(e))
 return redirect('grupos_admin')


@login_required
def persona_electoral(request,pid):
 api=SiraApi(request)
 try:
  p=api.get(f'/personas/{pid}')
  if request.method=='POST' and request.POST.get('accion')=='consultar':
   data=api.post(f'/electoral/consultas/persona/{pid}',{'nacionalidad':'V'})
  else:
   actual=api.get(f'/electoral/persona/{pid}')
   if actual.get('existe'):
    r=actual.get('registro',{});data={'indicadorRegistroExistente':r.get('indicador_registro_existente'),'nombres':r.get('nombres_fuente'),'apellidos':r.get('apellidos_fuente'),'mensajePantalla':'Los datos aquí presentados pudieran estar o no actualizados en relación con la base de datos del CNE.','datosElectorales':{'estado':r.get('estado'),'municipio':r.get('municipio'),'parroquia':r.get('parroquia'),'centroElectoral':r.get('centro_electoral')}}
   else:data=None
 except ApiError as e:messages.error(request,str(e));data=None;p={}
 return render(request,'core/electoral.html',{'p':p,'pid':pid,'r':data,'paso':2})

@login_required
def persona_electoral_declaracion(request,pid):
 api=SiraApi(request);actual=api.get(f'/electoral/persona/{pid}');p=api.get(f'/personas/{pid}');f=ElectoralDeclaracionForm(request.POST or None)
 if request.method=='POST' and f.is_valid():api.post(f'/electoral/persona/{pid}/declaracion',f.cleaned_data);messages.success(request,'Declaración electoral guardada y marcada para revisión.');return redirect('persona_grupos',pid=pid)
 return render(request,'core/electoral_declaracion.html',{'p':p,'pid':pid,'actual':actual.get('registro',{}),'form':f})


PUBLIC_STEPS=['personales','contacto','territorio','academico','electoral','grupos','finalizar']
def registro_publico_paso(request,token,seccion):
 if seccion not in PUBLIC_STEPS:return redirect('registro_publico_paso',token=token,seccion='personales')
 api=SiraApi(request)
 uso_id=request.session.get('registro_publico_uso_id') or 0
 try:
  ctx=api.get(f"/publico/invitaciones/{token}/contexto?usoId={uso_id}")
  if 'usoId' in ctx and not request.session.get('registro_publico_uso_id'):request.session['registro_publico_uso_id']=ctx['usoId']
 except ApiError as e:return render(request,'core/publico_asistente.html',{'error':str(e),'token':token,'seccion':seccion,'steps':PUBLIC_STEPS})
 form=form2=form_redes=None;catalogos={};codigos_catalogo=[];redes_list=[]
 try:
  if seccion=='personales':
   ns=api.get('/publico/invitaciones/catalogos/nacionalidades');sx=api.get('/publico/invitaciones/catalogos/sexos');p=ctx['persona']
   fn=formatear_fecha_es(p.get('fecha_nacimiento'))
   initial={'paisEmisorId':p.get('id_pais_emisor'),'tipoDocumentoId':p.get('id_tipo_documento'),'documentoNumero':p.get('documento_numero'),'primerNombre':p.get('primer_nombre'),'segundoNombre':p.get('segundo_nombre'),'primerApellido':p.get('primer_apellido'),'segundoApellido':p.get('segundo_apellido'),'aliasApodo':p.get('alias_apodo'),'sexoId':p.get('id_sexo'),'fechaNacimiento':fn,'nacionalidadCatalogoId':p.get('id_nacionalidad_catalogo'),'consentimientoDatos':True}
   try:tipos_doc=api.get('/publico/invitaciones/tipos-documento')
   except Exception:tipos_doc=[]
   form=IdentificacionForm(request.POST or None,initial=initial,nacionalidades=choices(ns,'id_nacionalidad_catalogo','descripcion'),sexos=choices(sx,'id_sexo','descripcion'),tipos_documento=tipos_doc)
   if request.method=='POST' and form.is_valid():
    api.put(f'/publico/invitaciones/{token}/personales?usoId={request.session.get("registro_publico_uso_id","")}',payload_persona(form.cleaned_data))
    return redirect('registro_publico_paso',token=token,seccion='contacto')
  elif seccion=='contacto':
   tipos=api.get('/publico/invitaciones/tipos-contacto');codigos=api.get('/publico/invitaciones/codigos-telefonicos');codigos_catalogo=codigos
   usoId=request.session.get("registro_publico_uso_id","")
   try:redes_list=api.get(f'/publico/invitaciones/{token}/redes-sociales?usoId={usoId}')
   except ApiError:redes_list=[]
   redes_init={}
   for r in redes_list:
    t=r.get('tipo','').lower()
    if t=='x':redes_init['xTwitter']=r.get('valor','')
    else:redes_init[t]=r.get('valor','')
   try:paises_tel=api.get('/publico/invitaciones/paises-telefono')
   except Exception:paises_tel=[]
   form=TelefonoForm(request.POST if request.POST.get('accion')=='telefono' else None,tipos=choices(tipos,'id_tipo_contacto','descripcion'),codigos=[(x['id_codigo_telefonico'],f"{x['codigo_pais']} {x['codigo_area_operador']}") for x in codigos],paises_telefono=paises_tel)
   form2=CorreoForm(request.POST if request.POST.get('accion')=='correo' else None,prefix='correo')
   form_redes=RedSocialForm(request.POST if request.POST.get('accion')=='redes' else None,initial=redes_init)
   if request.method=='POST':
    accion=request.POST.get('accion')
    if accion=='telefono' and form.is_valid():
     api.post(f'/publico/invitaciones/{token}/telefono?usoId={usoId}',form.cleaned_data);return redirect('registro_publico_paso',token=token,seccion='contacto')
    if accion=='correo' and form2.is_valid():
     api.post(f'/publico/invitaciones/{token}/correo?usoId={usoId}',form2.cleaned_data);return redirect('registro_publico_paso',token=token,seccion='contacto')
    if accion=='redes' and form_redes.is_valid():
     api.put(f'/publico/invitaciones/{token}/redes-sociales?usoId={usoId}',form_redes.cleaned_data);messages.success(request,'Redes sociales actualizadas.');return redirect('registro_publico_paso',token=token,seccion='contacto')
    if accion=='borrar_telefono' and request.POST.get('id'):
     api.delete(f'/publico/invitaciones/{token}/telefono/{request.POST.get("id")}?usoId={usoId}');return redirect('registro_publico_paso',token=token,seccion='contacto')
    if accion=='borrar_correo' and request.POST.get('id'):
     api.delete(f'/publico/invitaciones/{token}/correo/{request.POST.get("id")}?usoId={usoId}');return redirect('registro_publico_paso',token=token,seccion='contacto')
  elif seccion=='territorio':
   g=ctx.get('residencia') or {};src=request.POST if request.method=='POST' else g
   def vv(n,o):return src.get(n) or src.get(o) or ''
   ids={'paisId':vv('paisId','id_pais'),'estadoId':vv('estadoId','id_estado'),'ciudadId':vv('ciudadId','id_ciudad'),'municipioId':vv('municipioId','id_municipio'),'parroquiaId':vv('parroquiaId','id_parroquia'),'tipoSectorId':vv('tipoSectorId','id_tipo_sector_geografico'),'sectorId':vv('sectorId','id_sector_geografico'),'codigoPostalId':vv('codigoPostalId','id_codigo_postal')}
   if not ids['paisId']: ids['paisId']=str(ctx.get('paisId') or '1')
   pais=api.get('/publico/invitaciones/geografia/paises');tipsec=api.get('/publico/invitaciones/geografia/tipos-sector');est=api.get('/publico/invitaciones/geografia/estados',{'paisId':ids['paisId']}) if ids['paisId'] else [];ciu=api.get('/publico/invitaciones/geografia/ciudades',{'estadoId':ids['estadoId']}) if ids['estadoId'] else [];mun=api.get('/publico/invitaciones/geografia/municipios',{'ciudadId':ids['ciudadId']}) if ids['ciudadId'] else [];par=api.get('/publico/invitaciones/geografia/parroquias',{'municipioId':ids['municipioId']}) if ids['municipioId'] else [];sec=api.get('/publico/invitaciones/geografia/sectores',{'estadoId':ids['estadoId'],'ciudadId':ids['ciudadId'],'municipioId':ids['municipioId'],'parroquiaId':ids['parroquiaId'],'tipoSectorId':ids['tipoSectorId']}) if ids['tipoSectorId'] else [];cp=api.get('/publico/invitaciones/geografia/codigos-postales',{'sectorId':ids['sectorId']}) if ids['sectorId'] else []
   if ids['sectorId'] and not ids['codigoPostalId'] and len(cp)==1:ids['codigoPostalId']=str(cp[0]['id_codigo_postal'])
   ch={'paisId':choices(pais,'id_pais','desc_pais'),'estadoId':choices(est,'id_estado','desc_estado'),'ciudadId':choices(ciu,'id_ciudad','desc_ciudad'),'municipioId':choices(mun,'id_municipio','desc_municipio'),'parroquiaId':choices(par,'id_parroquia','desc_parroquia'),'tipoSectorId':choices(tipsec,'id_tipo_sector_geografico','desc_tipo_sector_geografico'),'sectorId':choices(sec,'id_sector_geografico','desc_sector_geografico'),'codigoPostalId':choices(cp,'id_codigo_postal','codigo_postal')}
   ubi_val=src.get('ubicacion') or g.get('ubicacion') or ctx.get('ubicacion') or ctx.get('ubicacionReferencia') or ctx.get('persona',{}).get('ubicacionReferencia','')
   pais_val=src.get('paisNombre') or src.get('pais') or g.get('desc_pais') or ctx.get('paisNombre') or ctx.get('pais') or 'Venezuela'
   initial={**ids,'direccionComplementaria':src.get('direccionComplementaria') or g.get('direccion_complementaria',''),'ubicacion':ubi_val,'paisNombre':pais_val}
   form=ResidenciaForm(request.POST or None,initial=initial,choices=ch)
   if request.method=='POST' and request.POST.get('accion')=='guardar' and form.is_valid():
    payload_terr=dict(form.cleaned_data)
    payload_terr['paisNombre']=request.POST.get('paisNombre') or form.cleaned_data.get('paisNombre') or pais_val
    api.put(f'/publico/invitaciones/{token}/territorio?usoId={request.session.get("registro_publico_uso_id","")}',payload_terr)
    return redirect('registro_publico_paso',token=token,seccion='academico')
  elif seccion=='academico':
   d=ctx.get('academico') or {}
   try:titulos=choices(api.get('/publico/invitaciones/catalogos/titulos'),'id_titulo','descripcion')
   except ApiError:titulos=[]
   c={'niveles':choices(api.get('/publico/invitaciones/catalogos/niveles'),'id_nivel','descripcion'),'especialidades':choices(api.get('/publico/invitaciones/catalogos/especialidades'),'id_especialidad','descripcion'),'honores':choices(api.get('/publico/invitaciones/catalogos/honores'),'id_honor','descripcion'),'disponibilidades':choices(api.get('/publico/invitaciones/catalogos/disponibilidades'),'id_disponibilidad','descripcion'),'modalidades':choices(api.get('/publico/invitaciones/catalogos/modalidades'),'id_modalidad','descripcion'),'titulos':titulos}
   initial={'nivelId':d.get('id_nivel'),'titulo1Id':d.get('id_titulo_1') or '','titulo':d.get('titulo'),'especialidadId':d.get('id_especialidad'),'titulo2Id':d.get('id_titulo_2') or '','titulo2':d.get('titulo_2'),'especialidad2Id':d.get('id_especialidad_2'),'postgrado':d.get('postgrado')=='S','descripcionPostgrado':d.get('descripcion_postgrado'),'doctorado':d.get('doctorado')=='S','descripcionDoctorado':d.get('descripcion_doctorado'),'magister':d.get('magister')=='S','descripcionMagister':d.get('descripcion_magister'),'honorId':d.get('id_honor'),'ocupacion1':d.get('ocupacion_1'),'ocupacion2':d.get('ocupacion_2'),'ocupacion3':d.get('ocupacion_3'),'disponibilidadId':d.get('id_disponibilidad'),'modalidadId':d.get('id_modalidad'),'whatsapp':d.get('whatsapp'),'facebook':d.get('facebook'),'instagram':d.get('instagram'),'youtube':d.get('youtube'),'xTwitter':d.get('x_twitter'),'observacion':d.get('observacion')}
   form=AcademicoForm(request.POST or None,initial=initial,c=c)
   if request.method=='POST' and form.is_valid():api.put(f'/publico/invitaciones/{token}/academico?usoId={request.session.get("registro_publico_uso_id","")}',form.cleaned_data);return redirect('registro_publico_paso',token=token,seccion='electoral')
  elif seccion=='grupos':
   form=GrupoPersonaForm(request.POST or None,initial={'otroGrupo':ctx.get('otroGrupo','')})
   form.fields['grupoId'].choices=choices(ctx.get('catalogoGrupos',[]),'id_grupo','descripcion')
   if request.method=='POST' and form.is_valid():
    gid=form.cleaned_data.get('grupoId')
    og=form.cleaned_data.get('otroGrupo')
    payload={'otroGrupo':og}
    if gid:payload['grupoId']=gid
    api.post(f"/publico/invitaciones/{token}/grupos?usoId={request.session.get('registro_publico_uso_id','')}",payload)
    return redirect('registro_publico_paso',token=token,seccion='grupos')
  elif seccion=='finalizar' and request.method=='POST':api.post(f'/publico/invitaciones/{token}/finalizar?usoId={request.session.get("registro_publico_uso_id","")}',{});ctx['finalizado']=True
 except ApiError as e:messages.error(request,str(e))
 return render(request,'core/publico_asistente.html',{'token':token,'seccion':seccion,'steps':PUBLIC_STEPS,'ctx':ctx,'form':form,'form2':form2,'form_redes':form_redes,'redes_list':redes_list,'codigos_catalogo':codigos_catalogo})
def registro_publico_grupo_quitar(request,token,gid):
 if request.method=='POST':SiraApi(request).delete(f"/publico/invitaciones/{token}/grupos/{gid}?usoId={request.session.get('registro_publico_uso_id','')}")
 return redirect('registro_publico_paso',token=token,seccion='grupos')


def registro_publico_salir(request,token):
 api=SiraApi(request);uso=request.session.get('registro_publico_uso_id')
 if request.method=='POST' and uso:
  try:api.post(f'/publico/invitaciones/{token}/finalizar?usoId={uso}',{})
  except ApiError as e:messages.error(request,str(e));return redirect('registro_publico_paso',token=token,seccion='finalizar')
 for k in ('registro_publico_token','registro_publico_persona_id','registro_publico_uso_id','registro_publico_resultado'):request.session.pop(k,None)
 return render(request,'core/publico_salida.html')


@login_required
def usuario_gestion(request,uid=None):
 api=SiraApi(request);u=api.get(f'/usuarios/{uid}') if uid else None;personas=api.get('/usuarios/catalogos/personas-sin-usuario');roles=api.get('/usuarios/catalogos/roles');initial={'personaId':u.get('id_persona'),'username':u.get('username'),'correoAcceso':u.get('correo_acceso'),'estado':u.get('estado'),'bloqueado':u.get('bloqueado')=='S'} if u else {};f=UsuarioGestionForm(request.POST or None,initial=initial);f.fields['personaId'].choices=[(str(x['id_persona']),f"{x['nombre']} · {x['documento_numero']}") for x in personas]+([(str(u['id_persona']),u['persona'])] if u else []);asignados=[str(x['id_rol']) for x in u.get('roles',[])] if u else []
 if request.method=='POST' and f.is_valid():
  d=f.cleaned_data;d['roles']=[int(x) for x in request.POST.getlist('roles')];api.put(f'/usuarios/{uid}',d) if uid else api.post('/usuarios',d);messages.success(request,'Usuario guardado.');return redirect('usuarios')
 return render(request,'core/usuario_gestion.html',{'form':f,'usuario':u,'roles':roles,'asignados':asignados})
@login_required
def usuario_password(request,uid):
 f=PasswordForm(request.POST or None)
 if request.method=='POST' and f.is_valid():SiraApi(request).post(f'/usuarios/{uid}/password',{'password':f.cleaned_data['password']});messages.success(request,'Contraseña actualizada.');return redirect('usuarios')
 return render(request,'core/usuario_password.html',{'form':f})
@login_required
def usuario_eliminar(request,uid):
 if request.method=='POST':
  try:SiraApi(request).delete(f'/usuarios/{uid}');messages.success(request,'Usuario eliminado.')
  except ApiError as e:messages.error(request,str(e))
 return redirect('usuarios')
@login_required
def roles(request):return render(request,'core/roles.html',{'rows':SiraApi(request).get('/usuarios/roles')})
@login_required
def rol_permisos(request,rid):
 api=SiraApi(request)
 if request.method=='POST':api.put(f'/usuarios/roles/{rid}/permisos',{'permisos':[int(x) for x in request.POST.getlist('permisos')]});messages.success(request,'Permisos guardados.');return redirect('roles')
 return render(request,'core/rol_permisos.html',{'data':api.get(f'/usuarios/roles/{rid}/permisos')})
