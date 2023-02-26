from django.contrib import admin
from .models import Perfil
from .views import reporte_usuarios

admin.site.register_view('reporte-usuarios', 'Reporte de usuarios', view=reporte_usuarios)

# Register your models here.
admin.site.register(Perfil)
