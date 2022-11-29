from django.conf.urls import url
from django.urls import path, include
from .views import (
    VoucherListApiView,
)

urlpatterns = [
    path('api', VoucherListApiView.as_view()),

]
