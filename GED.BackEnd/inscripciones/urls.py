from django.conf.urls import url
from django.urls import path, include
from .views import (
    InscripcionListApiView,
    InscripcionByUserApiView
)

urlpatterns = [
    path('api/', InscripcionListApiView.as_view()),
    path('api/<int:pk>/', InscripcionListApiView.as_view()),
    path('api/inscripcion/', InscripcionByUserApiView.as_view()),
]
