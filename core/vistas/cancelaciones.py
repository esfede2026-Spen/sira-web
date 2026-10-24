import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render


def _headers(request):
    token = request.session.get("access_token") or request.session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


@login_required
def bandeja_cancelaciones(request):
    base = settings.SIRA_API_URL.rstrip("/")
    params = {k: v for k, v in {
        "estado": request.GET.get("estado"),
        "tipoMotivoId": request.GET.get("tipo_motivo_id"),
    }.items() if v}
    try:
        solicitudes = requests.get(f"{base}/cancelaciones", params=params,
                                   headers=_headers(request), timeout=15).json()
        tipos = requests.get(f"{base}/cancelaciones/tipos-motivo",
                             headers=_headers(request), timeout=15).json()
    except requests.RequestException:
        solicitudes, tipos = [], []
        messages.error(request, "No fue posible consultar las solicitudes de cancelación.")
    return render(request, "administracion/cancelaciones.html", {
        "solicitudes": solicitudes, "tipos": tipos, "filtros": params
    })


@login_required
def clasificar_cancelacion(request, solicitud_id):
    if request.method != "POST":
        return redirect("cancelaciones_admin")
    base = settings.SIRA_API_URL.rstrip("/")
    payload = {
        "tipoMotivoId": request.POST.get("tipo_motivo_id"),
        "estado": request.POST.get("estado", "EN_REVISION"),
        "observacion": request.POST.get("observacion", ""),
    }
    try:
        respuesta = requests.put(f"{base}/cancelaciones/{solicitud_id}/clasificacion",
                                 json=payload, headers=_headers(request), timeout=15)
        respuesta.raise_for_status()
        messages.success(request, "La solicitud fue actualizada.")
    except requests.RequestException:
        messages.error(request, "No fue posible actualizar la solicitud.")
    return redirect("cancelaciones_admin")
