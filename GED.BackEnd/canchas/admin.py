from django.contrib import admin
from .models import Cancha
# Register your models here.
from .views import reporte_ingresos

admin.site.register_view('reporte-ingresos', 'Reporte de ingresos', view=reporte_ingresos)



admin.site.register(Cancha)
