from django.contrib import admin
from .models import Inscripcion
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import DateRangeFilterBuilder
# Register your models here.

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'jugador', 'partido', 'fecha_hora_inscripcion', 'fecha_hora_baja')
    search_fields = ('jugador__user__first_name', 'partido__fecha_hora','partido__cancha__deporte__descripcion')
    list_filter = (
        ('partido', RelatedDropdownFilter),
        ('jugador', RelatedDropdownFilter),
        ("fecha_hora_inscripcion", DateRangeFilterBuilder(title="Fecha de inscripcion")),
    )

    #search_fields = ('partido','jugador')
admin.site.register(Inscripcion, InscripcionAdmin)
