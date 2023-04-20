from django.conf.urls import url
from django.urls import path, include
from . import views
from .views import (
    PartidoListApiView,
    PartidoByUserApiView,
    InscritosByPartidoApiView,
    PartidoSemanaApiView,
)

urlpatterns = [
    path('api', PartidoListApiView.as_view()),
    path('api/partido/', PartidoByUserApiView.as_view()),
    path('api/partidoSemana/', PartidoSemanaApiView.as_view()),
    path('api/inscriptos/', InscritosByPartidoApiView.as_view()),
    path('partidos/', views.reporte_partidos_deportes, name='reporte_partidos_deportes'),
    path('partidos/', views.reporte_partidos_canchas, name='reporte_partidos_canchas'),

]
