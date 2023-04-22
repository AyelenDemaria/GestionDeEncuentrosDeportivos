from django.contrib import admin
from .models import Inscripcion
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, DropdownFilter
from rangefilter.filters import DateRangeFilterBuilder
# Register your models here.

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'jugador', 'partido', 'fecha_hora_inscripcion', 'fecha_hora_baja')
    search_fields = ('jugador__user__first_name', 'partido__fecha_hora','partido__cancha__cancha__deporte__descripcion')
    list_filter = (
        ('partido', RelatedDropdownFilter),
        ('partido__fecha_hora', DateRangeFilterBuilder(title="Fecha de partido")),
        ('partido__creador', RelatedDropdownFilter),
        ('jugador', RelatedDropdownFilter),
        ("fecha_hora_inscripcion", DateRangeFilterBuilder(title="Fecha de inscripcion")),
        ("fecha_hora_baja", DateRangeFilterBuilder(title="Fecha de baja")),
        ("partido__suspendido", DropdownFilter),
        ("partido__confirmado", DropdownFilter),
        ("fecha_hora_baja", admin.EmptyFieldListFilter)
    )

    #search_fields = ('partido','jugador')
admin.site.register(Inscripcion, InscripcionAdmin)
