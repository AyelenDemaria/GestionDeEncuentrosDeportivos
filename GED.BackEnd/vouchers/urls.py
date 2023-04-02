from django.conf.urls import url
from django.urls import path, include
from .views import (
    VoucherListApiView,
    VoucherByIDApiView,
)

urlpatterns = [
    path('api', VoucherListApiView.as_view()),
    path('api/voucher/', VoucherByIDApiView.as_view()),

]
