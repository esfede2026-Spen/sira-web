import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect,render

def brand(): return {"product_name":getattr(settings,"WTOGETHER_PRODUCT_NAME","Victoria"),"product_signature":getattr(settings,"WTOGETHER_PRODUCT_SIGNATURE","Victoria by WTogether"),"product_slogan":getattr(settings,"WTOGETHER_PRODUCT_SLOGAN","Connecting People, Building Communities"),"owner_name":getattr(settings,"WTOGETHER_OWNER_NAME","Infosoft, C.A."),"contact_email":getattr(settings,"WTOGETHER_CONTACT_EMAIL","sira.admin01@gmail.com")}
def headers(r):
 t=r.session.get("access_token") or r.session.get("token") or r.session.get("jwt") or r.session.get("auth_token")
 return {"Authorization":f"Bearer {t}"} if t else {}
def api(): return getattr(settings,"SIRA_API_URL","http://127.0.0.1:8080/api/v1").rstrip("/")
def quienes_somos(r): return render(r,"wtogether/quienes_somos.html",{"brand":brand()})
def contactanos(r): return render(r,"wtogether/contactanos.html",{"brand":brand()})
def cancelaciones(r):
 if not headers(r): return redirect("login")
 solicitudes=[];tipos=[]
 try:
  x=requests.get(api()+"/cancelaciones",headers=headers(r),timeout=15);x.raise_for_status();solicitudes=x.json()
  x=requests.get(api()+"/cancelaciones/tipos-motivo",headers=headers(r),timeout=15);x.raise_for_status();tipos=x.json()
 except (requests.RequestException,ValueError): messages.error(r,"No fue posible consultar las solicitudes.")
 return render(r,"wtogether/cancelaciones.html",{"brand":brand(),"solicitudes":solicitudes,"tipos":tipos})
def clasificar_cancelacion(r,solicitud_id):
 if r.method!="POST" or not headers(r): return redirect("login")
 try:
  x=requests.put(f"{api()}/cancelaciones/{solicitud_id}/clasificacion",json={"tipoMotivoId":r.POST.get("tipo_motivo_id"),"estado":r.POST.get("estado","EN_REVISION"),"observacion":r.POST.get("observacion","")},headers=headers(r),timeout=15);x.raise_for_status();messages.success(r,"Solicitud actualizada.")
 except requests.RequestException: messages.error(r,"No fue posible actualizar la solicitud.")
 return redirect("cancelaciones_admin")
