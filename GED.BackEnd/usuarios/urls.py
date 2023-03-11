from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PerfilListApiView,
    UserDataAPIView,
    ReporteByUserApiView,
    UserLoginApiView,
    PuntosUsertApiView,
    reporte_usuarios,
    UserLogoutApiView,
    CambioClaveAPIVIew,

)

#router = DefaultRouter()
#router.register(r'usuarios', UserLoginApiView, basename='usuarios')

urlpatterns = [
    path('api', PerfilListApiView.as_view()),
    path('api/usuario/', UserDataAPIView.as_view()),
    path('api/login/', UserLoginApiView.as_view()),
    path('api/logout/', UserLogoutApiView.as_view()),
    path('api/reporteUsuario/', ReporteByUserApiView.as_view()),
    path('api/puntosUsuario/', PuntosUsertApiView.as_view()),
    path('usuarios/', reporte_usuarios, name='reporte_usuarios'),
    path('api/cambiarClave/', CambioClaveAPIVIew.as_view()),

    #path('login/', include(router.urls))
    #path('api/login/', UsersLoginApiView.as_view({'get': 'list'}), basename='api/login/'),
    #path('api/login/', usuarios_views.UserLoginApiView, basename='usuarios'),
]
