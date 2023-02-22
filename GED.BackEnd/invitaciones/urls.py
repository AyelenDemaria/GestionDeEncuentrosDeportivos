from django.conf.urls import url
from django.urls import path, include
from .views import (
    InvitacionListApiView,
    AceptarInvitacionApiView,
    RechazarInvitacionApiView

)

urlpatterns = [
    path('api', InvitacionListApiView.as_view()),
    path('api/aceptarInvitacion/', AceptarInvitacionApiView.as_view()),
    path('api/rechazarInvitacion/', RechazarInvitacionApiView.as_view()),

]
