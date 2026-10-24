import os
import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger('sira.email')

def enviar_correo_bienvenida(request, datos_persona, token=None):
    """
    Procedimiento de envío de correo de bienvenida tras registro exitoso (Punto 9 - Sprint 2).
    Remitente: sira.admin01@gmail.com
    Destinatario: Correo de la persona registrada.
    """
    destinatario = datos_persona.get('correo') or datos_persona.get('correo_electronico')
    if not destinatario or not str(destinatario).strip():
        logger.warning("No se proporcionó correo para el envío de bienvenida.")
        return False

    destinatario = str(destinatario).strip()
    remitente = getattr(settings, 'DEFAULT_FROM_EMAIL', 'sira.admin01@gmail.com')
    if not remitente or remitente == 'webmaster@localhost':
        remitente = 'sira.admin01@gmail.com'

    # Extracción de parámetros
    p_nom = datos_persona.get('primerNombre') or datos_persona.get('primer_nombre') or ''
    p_ape = datos_persona.get('primerApellido') or datos_persona.get('primer_apellido') or ''
    nombre_completo = f"{p_nom} {p_ape}".strip() or "Ciudadano(a)"

    persona_id = datos_persona.get('personaId') or datos_persona.get('id_persona') or ''
    tipo_doc = datos_persona.get('tipoDocumentoId') or datos_persona.get('id_tipo_documento') or 'V'
    doc_num = datos_persona.get('documentoNumero') or datos_persona.get('documento_numero') or ''

    # Construcción de URLs
    if request:
        url_base = request.build_absolute_uri('/')[:-1]
    else:
        url_base = getattr(settings, 'WTOGETHER_PUBLIC_URL', 'http://127.0.0.1:8000').rstrip('/')

    url_actualizar = f"{url_base}/registro/editar?persona_id={persona_id}&tipo_documento={tipo_doc}&numero_documento={doc_num}&correo={destinatario}"
    if token:
        url_actualizar = f"{url_base}/registro/{token}/personales/"

    url_cancelar = f"{url_base}/suscripcion/cancelar?persona_id={persona_id}&tipo_documento={tipo_doc}&numero_documento={doc_num}&correo={destinatario}"

    asunto = "Bienvenido(a) a la Red de Personas SIRA"

    # Cuerpo en Texto Plano (Punto 9 Sprint 2)
    texto_plano = f"""Estimado(a) {nombre_completo},

Reciba un cordial saludo.

Le damos la bienvenida a la Red de Personas SIRA, un espacio diseñado para conectar personas, conocimientos, capacidades y experiencias en función de objetivos comunes y proyectos de interés colectivo.

Agradecemos sinceramente el tiempo dedicado a completar su registro y el aporte de información sobre sus conocimientos, experiencia y áreas de especialización. Su participación fortalece esta red y contribuye a identificar oportunidades de colaboración, organización e integración entre personas con intereses y capacidades afines.

Actualización de sus datos
Con el propósito de mantener su información vigente y precisa, podrá actualizar sus datos en cualquier momento utilizando el siguiente enlace seguro:

> Actualizar mis datos:
{url_actualizar}

Privacidad y protección de datos
La información suministrada por usted será tratada bajo principios de confidencialidad, integridad, disponibilidad y trazabilidad, alineados con las buenas prácticas promovidas por la familia de normas ISO/IEC 27000 para la gestión de la seguridad de la información.

Sus datos serán utilizados únicamente para:
- Gestionar y mantener su perfil dentro de la Red de Personas SIRA.
- Facilitar la conformación e integración de grupos de trabajo, comunidades, equipos técnicos o iniciativas relacionadas con sus áreas de experiencia y conocimiento.
- Enviarle información, invitaciones, oportunidades de participación, actividades o comunicaciones asociadas a los objetivos de la red.
- Mantener actualizada la información necesaria para el adecuado funcionamiento del sistema.

Sus datos personales no serán vendidos, transferidos ni compartidos con terceros para fines comerciales o distintos a los establecidos por la Red de Personas SIRA, salvo obligación legal expresa o autorización otorgada por usted.

Solicitud de cancelación de participación
Si en algún momento desea retirarse de la Red de Personas SIRA o solicitar que su perfil sea desactivado, podrá registrar una solicitud utilizando el siguiente enlace:

> Solicitar cancelación de participación:
{url_cancelar}

Su solicitud será registrada en el sistema para su procesamiento y seguimiento por el equipo responsable.

Le agradecemos nuevamente su registro y la confianza depositada en este proyecto.

Esperamos contar con su experiencia, conocimientos y participación en las distintas iniciativas que se desarrollen dentro de la Red de Personas SIRA.

Atentamente,
Equipo SIRA
Sistema Inteligente de Registro Activo
"""

    # Versión HTML enriquecida corporativa
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.6; margin: 0; padding: 20px; background-color: #f1f5f9; }}
    .container {{ max-width: 620px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 16px rgba(6,57,111,0.06); }}
    .header {{ background: linear-gradient(135deg, #06396f, #0057a8); padding: 24px 30px; color: #ffffff; }}
    .header h1 {{ margin: 0; font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }}
    .header p {{ margin: 4px 0 0; font-size: 13px; opacity: 0.9; }}
    .content {{ padding: 30px; font-size: 14.5px; color: #334155; }}
    .content p {{ margin: 0 0 16px; }}
    .btn {{ display: inline-block; padding: 11px 22px; background: #0057a8; color: #ffffff !important; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 14px; margin: 8px 0 20px; }}
    .btn-secondary {{ background: #f1f5f9; color: #64748b !important; border: 1px solid #cbd5e1; font-weight: 600; padding: 8px 16px; font-size: 13px; }}
    .callout {{ background: #f8fafc; border-left: 4px solid #0057a8; padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 20px 0; font-size: 13px; color: #475569; }}
    .footer {{ background: #f8fafc; padding: 20px 30px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b; text-align: center; }}
    ul {{ margin: 0 0 16px; padding-left: 22px; }}
    li {{ margin-bottom: 6px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Victoria · SIRA</h1>
      <p>Sistema Inteligente de Registro Activo · by WTogether</p>
    </div>
    <div class="content">
      <p>Estimado(a) <strong>{nombre_completo}</strong>,</p>
      <p>Reciba un cordial saludo.</p>
      <p>Le damos la bienvenida a la <strong>Red de Personas SIRA</strong>, un espacio diseñado para conectar personas, conocimientos, capacidades y experiencias en función de objetivos comunes y proyectos de interés colectivo.</p>
      <p>Agradecemos sinceramente el tiempo dedicado a completar su registro y el aporte de información sobre sus conocimientos, experiencia y áreas de especialización. Su participación fortalece esta red y contribuye a identificar oportunidades de colaboración, organización e integración entre personas con intereses y capacidades afines.</p>

      <h3 style="color: #06396f; margin: 24px 0 8px; font-size: 16px;">Actualización de sus datos</h3>
      <p>Con el propósito de mantener su información vigente y precisa, podrá actualizar sus datos en cualquier momento utilizando el siguiente enlace seguro:</p>
      <p><a href="{url_actualizar}" class="btn">&rarr; Actualizar mis datos</a></p>

      <div class="callout">
        <strong style="color: #06396f; display: block; margin-bottom: 6px;">Privacidad y protección de datos</strong>
        La información suministrada por usted será tratada bajo principios de confidencialidad, integridad, disponibilidad y trazabilidad, alineados con las buenas prácticas promovidas por la familia de normas ISO/IEC 27000 para la gestión de la seguridad de la información.
        <ul style="margin-top: 10px;">
          <li>Gestionar y mantener su perfil dentro de la Red de Personas SIRA.</li>
          <li>Facilitar la conformación e integración de grupos de trabajo, comunidades y equipos técnicos.</li>
          <li>Enviarle información, invitaciones o comunicaciones asociadas a los objetivos de la red.</li>
          <li>Mantener actualizada la información necesaria para el adecuado funcionamiento del sistema.</li>
        </ul>
        <span style="font-size: 11.5px; opacity: 0.85;">Sus datos personales no serán vendidos, transferidos ni compartidos con terceros para fines comerciales, salvo obligación legal o autorización expresa.</span>
      </div>

      <h3 style="color: #64748b; margin: 24px 0 8px; font-size: 14px;">Solicitud de cancelación de participación</h3>
      <p style="font-size: 13px; color: #64748b;">Si en algún momento desea retirarse de la Red de Personas SIRA o solicitar que su perfil sea desactivado, podrá registrar su solicitud en el siguiente enlace:</p>
      <p><a href="{url_cancelar}" class="btn btn-secondary">&rarr; Solicitar cancelación de participación</a></p>

      <p style="margin-top: 28px;">Atentamente,<br>
      <strong>Equipo SIRA</strong><br>
      <span style="color: #64748b; font-size: 13px;">Sistema Inteligente de Registro Activo</span></p>
    </div>
    <div class="footer">
      <strong>Victoria by WTogether 2.0</strong> · Tecnología desarrollada por Infosoft, C.A.<br>
      Mensaje automático generado para: {destinatario}
    </div>
  </div>
</body>
</html>
"""

    try:
        msg = EmailMultiAlternatives(
            subject=asunto,
            body=texto_plano,
            from_email=remitente,
            to=[destinatario]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"Correo de bienvenida enviado exitosamente a {destinatario}")
        return True
    except Exception as e:
        logger.error(f"Aviso en envío de correo de bienvenida a {destinatario}: {e}")
        return False
