from django.conf.urls import url
from django.urls import path, include
from .views import (
    PerfilListApiView,
)

urlpatterns = [
    path('api', PerfilListApiView.as_view()),

]
