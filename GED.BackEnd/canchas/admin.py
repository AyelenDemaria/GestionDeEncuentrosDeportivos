from django.contrib import admin
from .models import Cancha, CanchaPrecio
# Register your models here.
from .views import reporte_ingresos, reporte_ganancias
from rangefilter.filters import DateRangeFilterBuilder

admin.site.register_view('reporte-ingresos', 'Reporte de ingresos', view=reporte_ingresos)
admin.site.register_view('reporte-ganancias', 'Reporte de ganancias', view=reporte_ganancias)

class CanchaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'deporte')
    search_fields = ('deporte__descripcion',)

class CanchaPrecioAdmin(admin.ModelAdmin):
    list_display = ('id', 'cancha', 'fecha', 'abono_mensual','valor_uso','valor_referi')
    search_fields = ('cancha__nombre',)
    list_filter = (
        ("fecha", DateRangeFilterBuilder(title="Fecha de actualizacion")),
    )

admin.site.register(Cancha, CanchaAdmin)
admin.site.register(CanchaPrecio, CanchaPrecioAdmin)
