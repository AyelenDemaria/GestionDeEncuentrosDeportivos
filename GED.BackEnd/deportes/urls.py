from django.conf.urls import url
from django.urls import path, include
from .views import (
    DeporteListApiView,
)

urlpatterns = [
    path('api', DeporteListApiView.as_view()),
    
]
