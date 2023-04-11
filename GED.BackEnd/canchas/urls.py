from django.conf.urls import url
from django.urls import path, include
from .views import (
    CanchaListApiView,
    CanchaByDeporteListApiView,
    reporte_ingresos
)

urlpatterns = [
    path('api/', CanchaListApiView.as_view()),
    path('api/cancha_deporte/', CanchaByDeporteListApiView.as_view()),
    path('canchas/', reporte_ingresos, name='reporte_ingresos'),

]
