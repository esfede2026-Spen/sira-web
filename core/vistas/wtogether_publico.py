from django.conf import settings
from django.shortcuts import render


def quienes_somos(request):
    return render(request, "publico/quienes_somos.html")


def contactanos(request):
    return render(request, "publico/contactanos.html", {
        "contact_email": getattr(settings, "WTOGETHER_CONTACT_EMAIL", "contacto@wtogether.org")
    })
