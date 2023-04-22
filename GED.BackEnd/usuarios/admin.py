from django.contrib import admin
from .models import Perfil, PerfilAdmin
from .views import reporte_usuarios,reporte_vouchers

admin.site.register_view('reporte-usuarios', 'Reporte de partidos por usuario', view=reporte_usuarios)
admin.site.register_view('reporte-vouchers', 'Reporte de vouchers por usuario', view=reporte_vouchers)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'documento', 'telefono', 'fecha_nacimiento', 'sexo', 'puntos_acum')
    search_fields = ('user__first_name','user__last_name','documento',)

# Register your models here.
admin.site.register(Perfil, PerfilAdmin)
