from django.conf.urls import url
from django.urls import path, include
from .views import (
    Tipo_partidoListApiView,
)

urlpatterns = [
    path('api', Tipo_partidoListApiView.as_view()),

]
