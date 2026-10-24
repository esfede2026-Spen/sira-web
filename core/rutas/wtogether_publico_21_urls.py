from django.urls import path
from core.vistas.wtogether_publico_21 import quienes_somos,contactanos,cancelar_suscripcion
urlpatterns=[path('quienes-somos/',quienes_somos,name='quienes_somos'),path('contactanos/',contactanos,name='contactanos'),path('cancelar-suscripcion/',cancelar_suscripcion,name='cancelar_suscripcion')]
