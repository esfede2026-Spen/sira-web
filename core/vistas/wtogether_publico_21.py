from django.contrib import messages
from django.shortcuts import render

def quienes_somos(request): return render(request,'wtogether/quienes_somos.html')
def contactanos(request): return render(request,'wtogether/contactanos.html')
def cancelar_suscripcion(request):
    if request.method=='POST':
        messages.success(request,'Su solicitud fue recibida para revisión administrativa.')
    return render(request,'wtogether/cancelar_suscripcion.html')
