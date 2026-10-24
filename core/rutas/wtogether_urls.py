from django.urls import path
from core.vistas.wtogether import quienes_somos, contactanos, cancelaciones, clasificar_cancelacion
urlpatterns=[
 path("quienes-somos/",quienes_somos,name="quienes_somos"),
 path("contactanos/",contactanos,name="contactanos"),
 path("administracion/cancelaciones/",cancelaciones,name="cancelaciones_admin"),
 path("administracion/cancelaciones/<int:solicitud_id>/clasificar/",clasificar_cancelacion,name="cancelacion_clasificar"),
]
