from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('registros/', include('registros.urls')),
    path('vistas/', include('vistas.urls')),
    path('finanzas_personales/', include('finanzas_personales.urls')),
  
]
