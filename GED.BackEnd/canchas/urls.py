from django.conf.urls import url
from django.urls import path, include
from .views import (
    CanchaListApiView,
)

urlpatterns = [
    path('api/', CanchaListApiView.as_view()),

]
