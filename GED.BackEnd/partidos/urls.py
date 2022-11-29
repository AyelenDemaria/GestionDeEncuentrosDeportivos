from django.conf.urls import url
from django.urls import path, include
from .views import (
    PartidoListApiView,
)

urlpatterns = [
    path('api', PartidoListApiView.as_view()),

]
