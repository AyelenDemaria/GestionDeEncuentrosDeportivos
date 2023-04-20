from django.contrib import admin
from .models import Cancha, CanchaPrecio
# Register your models here.
from .views import reporte_ingresos

admin.site.register_view('reporte-ingresos', 'Reporte de ingresos', view=reporte_ingresos)

class CanchaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'deporte')
    search_fields = ('deporte__descripcion',)

class CanchaPrecioAdmin(admin.ModelAdmin):
    list_display = ('id', 'cancha', 'fecha', 'abono_mensual','valor_uso','valor_referi')
    search_fields = ('cancha',)

admin.site.register(Cancha, CanchaAdmin)
admin.site.register(CanchaPrecio, CanchaPrecioAdmin)
