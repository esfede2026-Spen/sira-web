from django import forms
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
 username=forms.CharField(label='Usuario o correo')
 password=forms.CharField(label='Contraseña',widget=forms.PasswordInput)
 captcha=forms.CharField(label='Código de seguridad',max_length=6,widget=forms.TextInput(attrs={'autocomplete':'off'}))
class IdentificacionForm(forms.Form):
 paisEmisorId=forms.IntegerField(initial=1,required=False,widget=forms.HiddenInput);tipoDocumentoId=forms.ChoiceField(label='Tipo de documento',initial=1);documentoNumero=forms.CharField(label='N.º documento',max_length=20,widget=forms.TextInput(attrs={'placeholder':'no. cedula','class':'form-input','inputmode':'numeric'}))
 primerNombre=forms.CharField(label='Primer nombre',max_length=100);segundoNombre=forms.CharField(label='Segundo nombre',max_length=100,required=False);primerApellido=forms.CharField(label='Primer apellido',max_length=100);segundoApellido=forms.CharField(label='Segundo apellido',max_length=100,required=False);aliasApodo=forms.CharField(label='Alias o apodo',max_length=100,required=False);fechaNacimiento=forms.DateField(label='Fecha de nacimiento',required=False,input_formats=['%d/%m/%Y','%Y-%m-%d'],widget=forms.TextInput(attrs={'placeholder':'DD/MM/AAAA','class':'field-fecha-nac','autocomplete':'off','maxlength':'10','inputmode':'numeric'}))
 nacionalidadCatalogoId=forms.ChoiceField(label='Nacionalidad');consentimientoDatos=forms.BooleanField(label='Acepto y doy consentimiento para el uso de mis datos',required=False);sexoId=forms.ChoiceField(label='Sexo', required=True, choices=(('', 'Seleccione…'), ('1', 'Femenino'), ('2', 'Masculino')));referidoId=forms.IntegerField(required=False,widget=forms.HiddenInput);nacionalidadId=forms.IntegerField(required=False,widget=forms.HiddenInput)
 def __init__(self,*a,nacionalidades=(),sexos=None,tipos_documento=None,**k):
  super().__init__(*a,**k)
  self.fields['nacionalidadCatalogoId'].choices=nacionalidades
  if sexos:
   self.fields['sexoId'].choices=[('','Seleccione…')]+[(str(k),v) for k,v in sexos]
  if tipos_documento:
   self.fields['tipoDocumentoId'].choices=[(str(t.get('id_tipo_documento', t.get('id', ''))), t.get('codigo', '')) for t in tipos_documento]
  else:
   self.fields['tipoDocumentoId'].choices=[('1', 'V'), ('3', 'E')]
class CorreoForm(forms.Form):correo=forms.EmailField(label='Correo electrónico',max_length=254);principal=forms.BooleanField(label='Correo principal',required=False,initial=True)
PAISES_TELEFONO = (
    ('+58', '+58 (Venezuela)'),
    ('+93', '+93 (Afganistán)'),
    ('+355', '+355 (Albania)'),
    ('+49', '+49 (Alemania)'),
    ('+376', '+376 (Andorra)'),
    ('+244', '+244 (Angola)'),
    ('+1268', '+1268 (Antigua y Barbuda)'),
    ('+966', '+966 (Arabia Saudita)'),
    ('+213', '+213 (Argelia)'),
    ('+54', '+54 (Argentina)'),
    ('+374', '+374 (Armenia)'),
    ('+61', '+61 (Australia)'),
    ('+43', '+43 (Austria)'),
    ('+994', '+994 (Azerbaiyán)'),
    ('+1242', '+1242 (Bahamas)'),
    ('+880', '+880 (Bangladés)'),
    ('+1246', '+1246 (Barbados)'),
    ('+973', '+973 (Baréin)'),
    ('+501', '+501 (Belice)'),
    ('+229', '+229 (Benín)'),
    ('+375', '+375 (Bielorrusia)'),
    ('+591', '+591 (Bolivia)'),
    ('+387', '+387 (Bosnia y Herzegovina)'),
    ('+267', '+267 (Botsuana)'),
    ('+55', '+55 (Brasil)'),
    ('+673', '+673 (Brunéi)'),
    ('+359', '+359 (Bulgaria)'),
    ('+226', '+226 (Burkina Faso)'),
    ('+257', '+257 (Burundi)'),
    ('+975', '+975 (Bután)'),
    ('+32', '+32 (Bélgica)'),
    ('+238', '+238 (Cabo Verde)'),
    ('+855', '+855 (Camboya)'),
    ('+237', '+237 (Camerún)'),
    ('+974', '+974 (Catar)'),
    ('+235', '+235 (Chad)'),
    ('+56', '+56 (Chile)'),
    ('+86', '+86 (China)'),
    ('+357', '+357 (Chipre)'),
    ('+57', '+57 (Colombia)'),
    ('+269', '+269 (Comoras)'),
    ('+850', '+850 (Corea del Norte)'),
    ('+82', '+82 (Corea del Sur)'),
    ('+225', '+225 (Costa de Marfil)'),
    ('+506', '+506 (Costa Rica)'),
    ('+385', '+385 (Croacia)'),
    ('+53', '+53 (Cuba)'),
    ('+45', '+45 (Dinamarca)'),
    ('+1767', '+1767 (Dominica)'),
    ('+593', '+593 (Ecuador)'),
    ('+20', '+20 (Egipto)'),
    ('+503', '+503 (El Salvador)'),
    ('+971', '+971 (Emiratos Árabes Unidos)'),
    ('+291', '+291 (Eritrea)'),
    ('+421', '+421 (Eslovaquia)'),
    ('+386', '+386 (Eslovenia)'),
    ('+34', '+34 (España)'),
    ('+372', '+372 (Estonia)'),
    ('+251', '+251 (Etiopía)'),
    ('+63', '+63 (Filipinas)'),
    ('+358', '+358 (Finlandia)'),
    ('+679', '+679 (Fiyi)'),
    ('+33', '+33 (Francia)'),
    ('+241', '+241 (Gabón)'),
    ('+220', '+220 (Gambia)'),
    ('+995', '+995 (Georgia)'),
    ('+233', '+233 (Ghana)'),
    ('+1473', '+1473 (Granada)'),
    ('+30', '+30 (Grecia)'),
    ('+502', '+502 (Guatemala)'),
    ('+224', '+224 (Guinea)'),
    ('+240', '+240 (Guinea Ecuatorial)'),
    ('+245', '+245 (Guinea-Bisáu)'),
    ('+592', '+592 (Guyana)'),
    ('+509', '+509 (Haití)'),
    ('+504', '+504 (Honduras)'),
    ('+36', '+36 (Hungría)'),
    ('+91', '+91 (India)'),
    ('+62', '+62 (Indonesia)'),
    ('+964', '+964 (Irak)'),
    ('+353', '+353 (Irlanda)'),
    ('+98', '+98 (Irán)'),
    ('+354', '+354 (Islandia)'),
    ('+972', '+972 (Israel)'),
    ('+39', '+39 (Italia)'),
    ('+1876', '+1876 (Jamaica)'),
    ('+81', '+81 (Japón)'),
    ('+962', '+962 (Jordania)'),
    ('+7', '+7 (Kazajistán)'),
    ('+254', '+254 (Kenia)'),
    ('+996', '+996 (Kirguistán)'),
    ('+686', '+686 (Kiribati)'),
    ('+965', '+965 (Kuwait)'),
    ('+856', '+856 (Laos)'),
    ('+266', '+266 (Lesoto)'),
    ('+371', '+371 (Letonia)'),
    ('+231', '+231 (Liberia)'),
    ('+218', '+218 (Libia)'),
    ('+423', '+423 (Liechtenstein)'),
    ('+370', '+370 (Lituania)'),
    ('+352', '+352 (Luxemburgo)'),
    ('+961', '+961 (Líbano)'),
    ('+389', '+389 (Macedonia del Norte)'),
    ('+261', '+261 (Madagascar)'),
    ('+60', '+60 (Malasia)'),
    ('+265', '+265 (Malaui)'),
    ('+960', '+960 (Maldivas)'),
    ('+356', '+356 (Malta)'),
    ('+223', '+223 (Malí)'),
    ('+212', '+212 (Marruecos)'),
    ('+230', '+230 (Mauricio)'),
    ('+222', '+222 (Mauritania)'),
    ('+691', '+691 (Micronesia)'),
    ('+373', '+373 (Moldavia)'),
    ('+976', '+976 (Mongolia)'),
    ('+382', '+382 (Montenegro)'),
    ('+258', '+258 (Mozambique)'),
    ('+95', '+95 (Myanmar)'),
    ('+52', '+52 (México)'),
    ('+377', '+377 (Mónaco)'),
    ('+264', '+264 (Namibia)'),
    ('+674', '+674 (Nauru)'),
    ('+977', '+977 (Nepal)'),
    ('+505', '+505 (Nicaragua)'),
    ('+234', '+234 (Nigeria)'),
    ('+47', '+47 (Noruega)'),
    ('+64', '+64 (Nueva Zelanda)'),
    ('+227', '+227 (Níger)'),
    ('+968', '+968 (Omán)'),
    ('+92', '+92 (Pakistán)'),
    ('+680', '+680 (Palaos)'),
    ('+507', '+507 (Panamá)'),
    ('+675', '+675 (Papúa Nueva Guinea)'),
    ('+595', '+595 (Paraguay)'),
    ('+31', '+31 (Países Bajos)'),
    ('+51', '+51 (Perú)'),
    ('+48', '+48 (Polonia)'),
    ('+351', '+351 (Portugal)'),
    ('+44', '+44 (Reino Unido)'),
    ('+236', '+236 (República Centroafricana)'),
    ('+420', '+420 (República Checa)'),
    ('+242', '+242 (República del Congo)'),
    ('+243', '+243 (República Democrática del Congo)'),
    ('+1809', '+1809 (República Dominicana)'),
    ('+250', '+250 (Ruanda)'),
    ('+40', '+40 (Rumania)'),
    ('+685', '+685 (Samoa)'),
    ('+1869', '+1869 (San Cristóbal y Nieves)'),
    ('+378', '+378 (San Marino)'),
    ('+1784', '+1784 (San Vicente y las Granadinas)'),
    ('+1758', '+1758 (Santa Lucía)'),
    ('+239', '+239 (Santo Tomé y Príncipe)'),
    ('+221', '+221 (Senegal)'),
    ('+381', '+381 (Serbia)'),
    ('+248', '+248 (Seychelles)'),
    ('+232', '+232 (Sierra Leona)'),
    ('+65', '+65 (Singapur)'),
    ('+963', '+963 (Siria)'),
    ('+252', '+252 (Somalia)'),
    ('+94', '+94 (Sri Lanka)'),
    ('+268', '+268 (Suazilandia)'),
    ('+27', '+27 (Sudáfrica)'),
    ('+249', '+249 (Sudán)'),
    ('+211', '+211 (Sudán del Sur)'),
    ('+46', '+46 (Suecia)'),
    ('+41', '+41 (Suiza)'),
    ('+597', '+597 (Surinam)'),
    ('+66', '+66 (Tailandia)'),
    ('+886', '+886 (Taiwán)'),
    ('+255', '+255 (Tanzania)'),
    ('+992', '+992 (Tayikistán)'),
    ('+670', '+670 (Timor Oriental)'),
    ('+228', '+228 (Togo)'),
    ('+676', '+676 (Tonga)'),
    ('+1868', '+1868 (Trinidad y Tobago)'),
    ('+993', '+993 (Turkmenistán)'),
    ('+90', '+90 (Turquía)'),
    ('+688', '+688 (Tuvalu)'),
    ('+216', '+216 (Túnez)'),
    ('+380', '+380 (Ucrania)'),
    ('+256', '+256 (Uganda)'),
    ('+598', '+598 (Uruguay)'),
    ('+998', '+998 (Uzbekistán)'),
    ('+678', '+678 (Vanuatu)'),
    ('+84', '+84 (Vietnam)'),
    ('+967', '+967 (Yemen)'),
    ('+253', '+253 (Yibuti)'),
    ('+260', '+260 (Zambia)'),
    ('+263', '+263 (Zimbabue)'),
)

class TelefonoForm(forms.Form):
    tipoContactoId = forms.ChoiceField(label='Tipo de teléfono')
    codigoPais = forms.ChoiceField(label='Código', initial='+58', choices=PAISES_TELEFONO, widget=forms.Select(attrs={'class': 'field-cod-pais'}))
    codigoArea = forms.CharField(label='Área', required=True, max_length=3, widget=forms.TextInput(attrs={'class': 'field-cod-area', 'placeholder': '412', 'maxlength': '3', 'autocomplete': 'off', 'inputmode': 'numeric'}))
    numero = forms.CharField(label='Teléfono:', min_length=7, max_length=7, widget=forms.TextInput(attrs={'class': 'field-telefono-num', 'inputmode': 'numeric', 'maxlength': '7', 'placeholder': '7 dígitos'}))
    extension = forms.CharField(label='Extensión', max_length=10, required=False)
    principal = forms.BooleanField(label='Teléfono principal', required=False)
    usaWhatsapp = forms.BooleanField(label='Usa WhatsApp', required=False)
    codigoTelefonicoId = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *a, tipos=(), codigos=(), paises_telefono=None, **k):
        super().__init__(*a, **k)
        if tipos:
            self.fields['tipoContactoId'].choices = tipos
        if paises_telefono:
            self.fields['codigoPais'].choices = [(p.get('codigo_pais', ''), f"{p.get('codigo_pais', '')} ({p.get('desc_pais', '')})") for p in paises_telefono]

    def clean(self):
        d = super().clean()
        area = (d.get('codigoArea') or '').strip().lstrip('0')
        num = ''.join(filter(str.isdigit, d.get('numero') or ''))
        if not area or len(area) != 3 or not area.isdigit():
            self.add_error('codigoArea', 'El código de área debe tener exactamente 3 dígitos.')
        if len(num) != 7:
            self.add_error('numero', 'El teléfono debe tener exactamente 7 dígitos.')
        d['codigoArea'] = area
        d['numero'] = num
        return d
class ResidenciaForm(forms.Form):
 paisId=forms.ChoiceField(label='País');estadoId=forms.ChoiceField(label='Estado',required=False);ciudadId=forms.ChoiceField(label='Ciudad',required=False);municipioId=forms.ChoiceField(label='Municipio',required=False);parroquiaId=forms.ChoiceField(label='Parroquia',required=False);tipoSectorId=forms.ChoiceField(label='Tipo de sector',required=False);sectorId=forms.ChoiceField(label='Sector',required=False);codigoPostalId=forms.ChoiceField(label='Código postal',required=False);direccionComplementaria=forms.CharField(label='Dirección complementaria',required=False,max_length=500,widget=forms.Textarea(attrs={'rows':3,'placeholder':'Calle, edificio, casa, punto de referencia'}));ubicacion=forms.CharField(label='Ubicación / Referencia geográfica',required=False,max_length=255,widget=forms.TextInput(attrs={'placeholder':'Ubicación o referencia geográfica'}));paisNombre=forms.CharField(label='País',required=False,max_length=100,widget=forms.TextInput(attrs={'placeholder':'Venezuela'}))
 def __init__(self,*a,c=None,choices=None,**k):super().__init__(*a,**k);choices=choices or {};[setattr(self.fields[f],'choices',choices.get(f,())) for f in ('paisId','estadoId','ciudadId','municipioId','parroquiaId','tipoSectorId','sectorId','codigoPostalId')]
class AcademicoForm(forms.Form):
 nivelId=forms.ChoiceField(label='Nivel académico',required=False)
 titulo1Id=forms.ChoiceField(label='Título 1',required=False)
 especialidadId=forms.ChoiceField(label='Especialidad 1',required=False)
 titulo2Id=forms.ChoiceField(label='Título 2',required=False)
 especialidad2Id=forms.ChoiceField(label='Especialidad 2',required=False)
 descripcionPostgrado=forms.CharField(label='Postgrado',required=False,max_length=250,widget=forms.TextInput(attrs={'placeholder':'Indique postgrado','list':'lista_especialidades_sug'}))
 descripcionDoctorado=forms.CharField(label='Doctorado',required=False,max_length=250,widget=forms.TextInput(attrs={'placeholder':'Indique doctorado','list':'lista_especialidades_sug'}))
 descripcionMagister=forms.CharField(label='Magíster',required=False,max_length=250,widget=forms.TextInput(attrs={'placeholder':'Indique magíster','list':'lista_especialidades_sug'}))
 honorId=forms.ChoiceField(label='Honor académico',required=False)
 ocupacion1=forms.CharField(label='Ocupación 1',required=False,max_length=180)
 ocupacion2=forms.CharField(label='Ocupación 2',required=False,max_length=180)
 ocupacion3=forms.CharField(label='Ocupación 3',required=False,max_length=180)
 disponibilidadId=forms.ChoiceField(label='Disponibilidad',required=False)
 modalidadId=forms.ChoiceField(label='Modalidad',required=False)
 observacion=forms.CharField(label='Observación',required=False,widget=forms.Textarea(attrs={'rows':3}))
 postgrado=forms.BooleanField(required=False,widget=forms.HiddenInput())
 doctorado=forms.BooleanField(required=False,widget=forms.HiddenInput())
 magister=forms.BooleanField(required=False,widget=forms.HiddenInput())

 def __init__(self,*a,c=None,**k):
  super().__init__(*a,**k)
  c=c or {}
  self.fields['nivelId'].choices=c.get('niveles',())
  self.fields['titulo1Id'].choices=c.get('titulos',())
  self.fields['titulo2Id'].choices=c.get('titulos',())
  self.fields['especialidadId'].choices=c.get('especialidades',())
  self.fields['especialidad2Id'].choices=c.get('especialidades',())
  self.fields['honorId'].choices=c.get('honores',())
  self.fields['disponibilidadId'].choices=c.get('disponibilidades',())
  self.fields['modalidadId'].choices=c.get('modalidades',())

 def clean(self):
  d=super().clean()
  dp=(d.get('descripcionPostgrado') or '').strip()
  dd=(d.get('descripcionDoctorado') or '').strip()
  dm=(d.get('descripcionMagister') or '').strip()
  d['postgrado']=bool(dp)
  d['doctorado']=bool(dd)
  d['magister']=bool(dm)
  return d

class RedSocialForm(forms.Form):
 facebook=forms.CharField(label='Facebook',required=False,max_length=250,widget=forms.TextInput(attrs={'placeholder':'https://facebook.com/usuario o @usuario'}))
 instagram=forms.CharField(label='Instagram',required=False,max_length=250,widget=forms.TextInput(attrs={'placeholder':'@usuario'}))
 youtube=forms.CharField(label='YouTube',required=False,max_length=250,widget=forms.TextInput(attrs={'placeholder':'@canal o URL'}))
 xTwitter=forms.CharField(label='X (Twitter)',required=False,max_length=250,widget=forms.TextInput(attrs={'placeholder':'@usuario'}))

class GrupoPersonaForm(forms.Form):
 grupoId=forms.ChoiceField(label='Grupo existente',required=False)
 otroGrupo=forms.CharField(label='Otro Grupo:',required=False,max_length=200,widget=forms.TextInput(attrs={'style':'text-transform: uppercase;','placeholder':'INDIQUE OTRO GRUPO NO LISTADO'}))
 def clean_otroGrupo(self):
  v=self.cleaned_data.get('otroGrupo')
  return v.strip().upper() if v else ''
 def clean(self):
  d=super().clean()
  if not d.get('grupoId') and not d.get('otroGrupo'):
   self.add_error('grupoId','Seleccione un grupo o indique uno nuevo en Otro Grupo.')
  return d
class UsuarioForm(forms.Form):
 username=forms.CharField(label='Usuario',max_length=100);correoAcceso=forms.EmailField(label='Correo',max_length=254);password=forms.CharField(label='Contraseña',widget=forms.PasswordInput);confirmar=forms.CharField(label='Confirmar',widget=forms.PasswordInput)
 def clean(self):d=super().clean();self.add_error('confirmar','Las contraseñas no coinciden.') if d.get('password')!=d.get('confirmar') else None;return d
class InvitacionForm(forms.Form):
 referidoId=forms.ChoiceField(label='Persona que invita (referente)')
 nombre=forms.CharField(label='Nombre del invitado (opcional)',required=False)
 apellido=forms.CharField(label='Apellido del invitado (opcional)',required=False)
 canal=forms.ChoiceField(label='Canal de envío',choices=(('ENLACE','Copiar enlace'),('WHATSAPP','WhatsApp'),('CORREO','Correo')))
 vigenciaHoras=forms.IntegerField(label='Vigencia (horas)',initial=72,min_value=1,max_value=720)
 notificarCorreo=forms.BooleanField(label='Notificar por correo electrónico al invitado si se especifica',required=False)
 def __init__(self,*a,personas=(),**k):super().__init__(*a,**k);self.fields['referidoId'].choices=personas


class IdentificacionInicialForm(forms.Form):
 paisEmisorId=forms.IntegerField(initial=1,widget=forms.HiddenInput)
 tipoDocumentoId=forms.ChoiceField(label='Tipo de documento',initial=1)
 documentoNumero=forms.CharField(label='N.º documento',max_length=20,widget=forms.TextInput(attrs={'placeholder':'no. cedula','class':'form-input','inputmode':'numeric'}))
 nacionalidadCatalogoId=forms.ChoiceField(label='Nacionalidad')
 consentimientoDatos=forms.BooleanField(label='Acepto y doy consentimiento para el uso de mis datos',required=True)
 def __init__(self,*a,nacionalidades=(),tipos_documento=None,**k):
  super().__init__(*a,**k)
  self.fields['nacionalidadCatalogoId'].choices=nacionalidades
  if tipos_documento:
   self.fields['tipoDocumentoId'].choices=[(str(t.get('id_tipo_documento', t.get('id', ''))), t.get('codigo', '')) for t in tipos_documento]
  else:
   self.fields['tipoDocumentoId'].choices=[('1', 'V'), ('3', 'E')]

class ElectoralDeclaracionForm(forms.Form):
 inscritoDeclarado=forms.ChoiceField(label='¿Está inscrito en el registro electoral?',choices=(('','Seleccione'),('S','Sí'),('N','No')),required=False)
 observacion=forms.CharField(label='Observación',required=False,max_length=500,widget=forms.Textarea(attrs={'rows':3}))


class RegistroPublicoInicialForm(forms.Form):
    tipoDocumentoId = forms.ChoiceField(label='Tipo de documento', initial=1)
    documentoNumero = forms.CharField(label='N.º de documento *', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'no. cedula', 'class': 'form-input', 'inputmode': 'numeric'}))
    nacionalidadCatalogoId = forms.IntegerField(initial=1, widget=forms.HiddenInput())
    codigoPais = forms.ChoiceField(label='Código *', initial='+58', choices=PAISES_TELEFONO, widget=forms.Select(attrs={'class': 'field-cod-pais', 'id': 'id_codigo_pais'}))
    codigoArea = forms.CharField(label='Área *', required=True, max_length=3, widget=forms.TextInput(attrs={'class': 'field-cod-area', 'placeholder': '412', 'maxlength': '3', 'autocomplete': 'off', 'inputmode': 'numeric', 'id': 'id_codigo_area'}))
    numero = forms.CharField(label='Teléfono *', min_length=7, max_length=7, widget=forms.TextInput(attrs={'class': 'field-telefono-num', 'inputmode': 'numeric', 'maxlength': '7', 'placeholder': '7 dígitos', 'id': 'id_numero'}))
    correo = forms.EmailField(label='Correo electrónico *', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'}))
    autorizaUbicacion = forms.BooleanField(label='Autorizo ubicación', required=False)
    ubicacion = forms.CharField(label='Ubicación (referencia opcional):', required=False, max_length=250, widget=forms.TextInput(attrs={'placeholder': 'Sector, ciudad o referencia', 'id': 'id_ubicacion'}))
    paisNombre = forms.CharField(label='País:', required=False, initial='Venezuela', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Venezuela', 'id': 'id_pais_nombre', 'class': 'form-input', 'style': 'font-weight: 600;'}))
    codigoPaisGeo = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_codigo_pais_geo'}))
    latitud = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_latitud'}))
    longitud = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_longitud'}))
    precisionMetros = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'id': 'id_precision_metros'}))
    consentimientoDatos = forms.BooleanField(label='Acepto y doy consentimiento para el uso de mis datos', required=True)
    captcha = forms.CharField(label='Código de seguridad *', max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-input'}))
    codigoTelefonicoId = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *a, tipos_documento=None, paises_telefono=None, codigos=(), **k):
        super().__init__(*a, **k)
        if tipos_documento:
            self.fields['tipoDocumentoId'].choices = [(str(t.get('id_tipo_documento', t.get('id', ''))), t.get('codigo', '')) for t in tipos_documento]
        else:
            self.fields['tipoDocumentoId'].choices = [('1', 'V'), ('3', 'E')]
        if paises_telefono:
            self.fields['codigoPais'].choices = [(p.get('codigo_pais', ''), f"{p.get('codigo_pais', '')} ({p.get('desc_pais', '')})") for p in paises_telefono]

    def clean(self):
        d = super().clean()
        area = (d.get('codigoArea') or '').strip().lstrip('0')
        num = ''.join(filter(str.isdigit, d.get('numero') or ''))
        if not area or len(area) != 3 or not area.isdigit():
            self.add_error('codigoArea', 'El código de área debe tener exactamente 3 dígitos.')
        if len(num) != 7:
            self.add_error('numero', 'El teléfono debe tener exactamente 7 dígitos.')
        d['codigoArea'] = area
        d['numero'] = num
        if not d.get('paisNombre'):
            d['paisNombre'] = 'Venezuela'
        d['codigoPaisGeo'] = d.get('paisNombre')
        return d

class UsuarioGestionForm(forms.Form):
 personaId=forms.ChoiceField(label='Persona');username=forms.CharField(label='Usuario',max_length=100);correoAcceso=forms.EmailField(label='Correo',required=False);estado=forms.ChoiceField(label='Estado',choices=(('ACTIVO','Activo'),('INACTIVO','Inactivo')));bloqueado=forms.BooleanField(label='Bloqueado',required=False);password=forms.CharField(label='Contraseña inicial',required=False,widget=forms.PasswordInput)
class PasswordForm(forms.Form):
 password=forms.CharField(label='Nueva contraseña',min_length=8,widget=forms.PasswordInput);confirmar=forms.CharField(label='Confirmar contraseña',widget=forms.PasswordInput)
 def clean(self):
  d=super().clean()
  if d.get('password')!=d.get('confirmar'):self.add_error('confirmar','Las contraseñas no coinciden.')
  return d
