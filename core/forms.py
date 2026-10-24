from django import forms
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
 username=forms.CharField(label='Usuario o correo')
 password=forms.CharField(label='Contraseña',widget=forms.PasswordInput)
 captcha=forms.CharField(label='Código de seguridad',max_length=6,widget=forms.TextInput(attrs={'autocomplete':'off'}))
class IdentificacionForm(forms.Form):
 paisEmisorId=forms.IntegerField(initial=1,required=False,widget=forms.HiddenInput);tipoDocumentoId=forms.IntegerField(label='Tipo de documento',initial=1,widget=forms.Select(choices=((1,'C · Cédula'),(2,'P · Pasaporte'))));documentoNumero=forms.CharField(label='N.º documento',max_length=20)
 primerNombre=forms.CharField(label='Primer nombre',max_length=100);segundoNombre=forms.CharField(label='Segundo nombre',max_length=100,required=False);primerApellido=forms.CharField(label='Primer apellido',max_length=100);segundoApellido=forms.CharField(label='Segundo apellido',max_length=100,required=False);aliasApodo=forms.CharField(label='Alias o apodo',max_length=100,required=False);fechaNacimiento=forms.DateField(label='Fecha de nacimiento',required=False,input_formats=['%d/%m/%Y','%Y-%m-%d'],widget=forms.TextInput(attrs={'placeholder':'DD/MM/AAAA','class':'field-fecha-nac','autocomplete':'off','maxlength':'10','inputmode':'numeric'}))
 nacionalidadCatalogoId=forms.ChoiceField(label='Nacionalidad');consentimientoDatos=forms.BooleanField(label='Acepto y doy consentimiento para el uso de mis datos',required=False);sexoId=forms.ChoiceField(label='Sexo', required=True, choices=(('', 'Seleccione…'), ('1', 'Femenino'), ('2', 'Masculino')));referidoId=forms.IntegerField(required=False,widget=forms.HiddenInput);nacionalidadId=forms.IntegerField(required=False,widget=forms.HiddenInput)
 def __init__(self,*a,nacionalidades=(),sexos=None,**k):
  super().__init__(*a,**k)
  self.fields['nacionalidadCatalogoId'].choices=nacionalidades
  if sexos:
   self.fields['sexoId'].choices=[('','Seleccione…')]+[(str(k),v) for k,v in sexos]
class CorreoForm(forms.Form):correo=forms.EmailField(label='Correo electrónico',max_length=254);principal=forms.BooleanField(label='Correo principal',required=False,initial=True)
PAISES_TELEFONO = (
    ('+58', '+58 (Venezuela)'),
    ('+1', '+1 (EE. UU. / Canadá)'),
    ('+34', '+34 (España)'),
    ('+57', '+57 (Colombia)'),
    ('+56', '+56 (Chile)'),
    ('+54', '+54 (Argentina)'),
    ('+51', '+51 (Perú)'),
    ('+52', '+52 (México)'),
    ('+507', '+507 (Panamá)'),
    ('+593', '+593 (Ecuador)'),
    ('+55', '+55 (Brasil)'),
    ('+598', '+598 (Uruguay)'),
    ('+595', '+595 (Paraguay)'),
    ('+591', '+591 (Bolivia)'),
    ('+506', '+506 (Costa Rica)'),
    ('+503', '+503 (El Salvador)'),
    ('+502', '+502 (Guatemala)'),
    ('+504', '+504 (Honduras)'),
    ('+505', '+505 (Nicaragua)'),
    ('+1809', '+1809 (Rep. Dominicana)'),
    ('+39', '+39 (Italia)'),
    ('+351', '+351 (Portugal)'),
    ('+33', '+33 (Francia)'),
    ('+49', '+49 (Alemania)'),
    ('+44', '+44 (Reino Unido)'),
)

class TelefonoForm(forms.Form):
    tipoContactoId = forms.ChoiceField(label='Tipo de teléfono')
    codigoPais = forms.ChoiceField(label='Código', initial='+58', choices=PAISES_TELEFONO, widget=forms.Select(attrs={'class': 'field-cod-pais'}))
    codigoArea = forms.CharField(label='', required=True, max_length=6, widget=forms.TextInput(attrs={'class': 'field-cod-area', 'placeholder': '412', 'list': 'lista_codigos_area_tel', 'autocomplete': 'off', 'inputmode': 'numeric'}))
    numero = forms.CharField(label='Teléfono:', min_length=6, max_length=15, widget=forms.TextInput(attrs={'class': 'field-telefono-num', 'inputmode': 'numeric', 'maxlength': '15', 'placeholder': 'Número'}))
    extension = forms.CharField(label='Extensión', max_length=10, required=False)
    principal = forms.BooleanField(label='Teléfono principal', required=False)
    usaWhatsapp = forms.BooleanField(label='Usa WhatsApp', required=False)
    codigoTelefonicoId = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *a, tipos=(), codigos=(), **k):
        super().__init__(*a, **k)
        if tipos:
            self.fields['tipoContactoId'].choices = tipos

    def clean(self):
        d = super().clean()
        pais = (d.get('codigoPais') or '+58').strip()
        area = (d.get('codigoArea') or '').strip().lstrip('0')
        num = ''.join(filter(str.isdigit, d.get('numero') or ''))
        if not area:
            self.add_error('codigoArea', 'Indique el código de área.')
        if pais == '+58':
            if len(num) != 7:
                self.add_error('numero', 'Para Venezuela el teléfono debe tener exactamente 7 dígitos.')
        else:
            if len(num) < 6 or len(num) > 12:
                self.add_error('numero', 'Para números internacionales introduzca entre 6 y 12 dígitos.')
        d['codigoArea'] = area
        d['numero'] = num
        return d
class ResidenciaForm(forms.Form):
 paisId=forms.ChoiceField(label='País');estadoId=forms.ChoiceField(label='Estado',required=False);ciudadId=forms.ChoiceField(label='Ciudad',required=False);municipioId=forms.ChoiceField(label='Municipio',required=False);parroquiaId=forms.ChoiceField(label='Parroquia',required=False);tipoSectorId=forms.ChoiceField(label='Tipo de sector',required=False);sectorId=forms.ChoiceField(label='Sector',required=False);codigoPostalId=forms.ChoiceField(label='Código postal',required=False);direccionComplementaria=forms.CharField(label='Dirección complementaria',required=False,max_length=500,widget=forms.Textarea(attrs={'rows':3,'placeholder':'Calle, edificio, casa, punto de referencia'}));ubicacion=forms.CharField(label='Ubicación / Referencia geográfica',required=False,max_length=255,widget=forms.TextInput(attrs={'placeholder':'Ubicación o referencia geográfica'}))
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
 tipoDocumentoId=forms.IntegerField(label='Tipo de documento',initial=1,widget=forms.Select(choices=((1,'C · Cédula'),(2,'P · Pasaporte'))))
 documentoNumero=forms.CharField(label='N.º documento',max_length=20)
 nacionalidadCatalogoId=forms.ChoiceField(label='Nacionalidad')
 consentimientoDatos=forms.BooleanField(label='Acepto y doy consentimiento para el uso de mis datos',required=True)
 def __init__(self,*a,nacionalidades=(),**k):super().__init__(*a,**k);self.fields['nacionalidadCatalogoId'].choices=nacionalidades

class ElectoralDeclaracionForm(forms.Form):
 inscritoDeclarado=forms.ChoiceField(label='¿Está inscrito en el registro electoral?',choices=(('','Seleccione'),('S','Sí'),('N','No')),required=False)
 observacion=forms.CharField(label='Observación',required=False,max_length=500,widget=forms.Textarea(attrs={'rows':3}))


class RegistroPublicoInicialForm(forms.Form):
    tipoDocumentoId = forms.IntegerField(label='Tipo de documento', initial=1, widget=forms.Select(choices=((1, 'C · Cédula'), (2, 'P · Pasaporte'))))
    documentoNumero = forms.CharField(label='N.º documento', max_length=20, widget=forms.TextInput(attrs={'inputmode': 'numeric'}))
    nacionalidadCatalogoId = forms.IntegerField(initial=1, widget=forms.HiddenInput())
    codigoPais = forms.ChoiceField(label='Código', initial='+58', choices=PAISES_TELEFONO, widget=forms.Select(attrs={'class': 'field-cod-pais'}))
    codigoArea = forms.CharField(label='', required=True, max_length=6, widget=forms.TextInput(attrs={'class': 'field-cod-area', 'placeholder': '412', 'list': 'lista_codigos_area', 'autocomplete': 'off', 'inputmode': 'numeric'}))
    numero = forms.CharField(label='Teléfono:', min_length=6, max_length=15, widget=forms.TextInput(attrs={'class': 'field-telefono-num', 'inputmode': 'numeric', 'maxlength': '15', 'placeholder': 'Número'}))
    correo = forms.EmailField(label='Correo electrónico', max_length=254)
    autorizaUbicacion = forms.BooleanField(label='Autorizo ubicación', required=False)
    ubicacion = forms.CharField(label='Ubicación (referencia opcional)', required=False, max_length=250, widget=forms.TextInput(attrs={'placeholder': 'Sector, ciudad o referencia'}))
    latitud = forms.CharField(required=False, widget=forms.HiddenInput())
    longitud = forms.CharField(required=False, widget=forms.HiddenInput())
    consentimientoDatos = forms.BooleanField(label='Acepto y doy consentimiento para el uso de mis datos', required=True)
    captcha = forms.CharField(label='Código de seguridad', max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    codigoTelefonicoId = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *a, codigos=(), **k):
        super().__init__(*a, **k)

    def clean(self):
        d = super().clean()
        pais = (d.get('codigoPais') or '+58').strip()
        area = (d.get('codigoArea') or '').strip().lstrip('0')
        num = ''.join(filter(str.isdigit, d.get('numero') or ''))
        if not area:
            self.add_error('codigoArea', 'Indique el código de área.')
        if pais == '+58':
            if len(num) != 7:
                self.add_error('numero', 'Para Venezuela el teléfono debe tener exactamente 7 dígitos.')
        else:
            if len(num) < 6 or len(num) > 12:
                self.add_error('numero', 'Para números internacionales introduzca entre 6 y 12 dígitos.')
        d['codigoArea'] = area
        d['numero'] = num
        return d

class UsuarioGestionForm(forms.Form):
 personaId=forms.ChoiceField(label='Persona');username=forms.CharField(label='Usuario',max_length=100);correoAcceso=forms.EmailField(label='Correo',required=False);estado=forms.ChoiceField(label='Estado',choices=(('ACTIVO','Activo'),('INACTIVO','Inactivo')));bloqueado=forms.BooleanField(label='Bloqueado',required=False);password=forms.CharField(label='Contraseña inicial',required=False,widget=forms.PasswordInput)
class PasswordForm(forms.Form):
 password=forms.CharField(label='Nueva contraseña',min_length=8,widget=forms.PasswordInput);confirmar=forms.CharField(label='Confirmar contraseña',widget=forms.PasswordInput)
 def clean(self):
  d=super().clean()
  if d.get('password')!=d.get('confirmar'):self.add_error('confirmar','Las contraseñas no coinciden.')
  return d
