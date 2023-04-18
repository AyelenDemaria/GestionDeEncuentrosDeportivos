from django.conf.urls import url
from django.urls import path, include
from . import views
from .views import (
    CanchaListApiView,
    CanchaByDeporteListApiView,
)

urlpatterns = [
    path('api/', CanchaListApiView.as_view()),
    path('api/cancha_deporte/', CanchaByDeporteListApiView.as_view()),
    path('canchas/', views.reporte_ingresos, name='reporte_ingresos'),
]
