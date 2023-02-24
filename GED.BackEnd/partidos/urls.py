from django.conf.urls import url
from django.urls import path, include
from .views import (
    PartidoListApiView,
    PartidoByUserApiView,
    InscritosByPartidoApiView,
)

urlpatterns = [
    path('api', PartidoListApiView.as_view()),
    path('api/partido/', PartidoByUserApiView.as_view()),
    path('api/inscriptos/', InscritosByPartidoApiView.as_view()),

]
