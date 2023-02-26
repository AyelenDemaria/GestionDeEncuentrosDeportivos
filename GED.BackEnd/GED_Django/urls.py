"""GED_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.sites.site = admin.site
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('deportes/', include('deportes.urls')),
    path('canchas/', include('canchas.urls')),
    path('tipos_partidos/', include('tipos_partidos.urls')),
    path('vouchers/', include('vouchers.urls')),
    path('partidos/', include('partidos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('invitaciones/', include('invitaciones.urls')),
]
