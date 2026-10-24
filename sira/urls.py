from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("", include("core.rutas.wtogether_urls")),
    path('', include('core.rutas.wtogether_urls')),
    path('', include('core.rutas.wtogether_publico_21_urls')),
]