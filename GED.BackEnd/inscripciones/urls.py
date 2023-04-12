from django.conf.urls import url
from django.urls import path, include
from .views import (
    InscripcionListApiView,
    InscripcionByUserApiView,
    InscriptosByPartidoApiView,
    PartidosSuspendidosApiView
)

urlpatterns = [
    path('api/', InscripcionListApiView.as_view()),
    path('api/<int:pk>/', InscripcionListApiView.as_view()),
    path('api/inscripcion/', InscripcionByUserApiView.as_view()),
    path('api/inscriptos/', InscriptosByPartidoApiView.as_view()),
    path('api/partidos_suspendidos/', PartidosSuspendidosApiView.as_view()),

]
