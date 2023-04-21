from django.contrib import admin
from .models import Partido
from inscripciones.models import Inscripcion
from usuarios.models import Perfil
from django.utils import timezone
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter,  DropdownFilter, ChoiceDropdownFilter
from rangefilter.filters import DateRangeFilterBuilder
from .views import reporte_partidos_deportes, reporte_partidos_canchas, reporte_partidos_tipos

admin.site.register_view('reporte-partidos-deportes', 'Reporte de partidos por deporte', view=reporte_partidos_deportes)
admin.site.register_view('reporte-partidos-canchas', 'Reporte de partidos por cancha', view=reporte_partidos_canchas)
admin.site.register_view('reporte-partidos-tipos', 'Reporte de partidos por tipo', view=reporte_partidos_tipos)

class PartidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_hora', 'cant_jugadores', 'tipo_partido', 'creador', 'cancha', 'suspendido', 'fecha_hora_suspendido','confirmado','fecha_hora_confirmado')
    search_fields = ('cancha__cancha__nombre', 'cancha__cancha__deporte__descripcion', 'creador__user__first_name')
    list_filter = (
        ('cancha__cancha', RelatedDropdownFilter),
        ('cancha__cancha__deporte', RelatedDropdownFilter),
        ('tipo_partido', RelatedDropdownFilter),
        ('creador', RelatedDropdownFilter),
        ("fecha_hora", DateRangeFilterBuilder(title="Fecha del partido")),
        ("suspendido", DropdownFilter),
        ("confirmado", DropdownFilter),
    )
    exclude = ('fecha_hora_suspendido', 'fecha_hora_confirmado')
    #readonly_fields = self.get_readonly(self, request)
    def get_readonly_fields(self,request, obj=None):
        fecha_hora_partido = timezone.localtime(obj.fecha_hora)
        print("fecha y hora partido: ",fecha_hora_partido)
        fecha_hora_actual = timezone.localtime(timezone.now())
        print("fecha y hora actual: ",fecha_hora_actual)
        if (fecha_hora_actual <= fecha_hora_partido) or (obj.confirmado == False and obj.fecha_hora_confirmado is not None and fecha_hora_partido < fecha_hora_actual) or obj.suspendido==True:
            #exclude = ('confirmado')
            #readonly_fields = ["confirmado"]
            return  ["confirmado"]
        else:
            return []

    def save_model(self, request, obj, form, change):
        fecha_hora_partido = timezone.localtime(obj.fecha_hora)
        #print("fecha y hora partido: ",fecha_hora_partido)
        fecha_hora_actual = timezone.localtime(timezone.now())
        #print("fecha y hora actual: ",fecha_hora_actual)
        if obj.confirmado == False and obj.fecha_hora_confirmado is None and fecha_hora_partido < fecha_hora_actual:
            print("partido", obj.id)
            obj.fecha_hora_confirmado = timezone.localtime(timezone.now())
            inscripciones = Inscripcion.objects.filter(partido_id = obj.id)
            if inscripciones:
                for i in inscripciones:
                    perfil = Perfil.objects.get(id=i.jugador_id)
                    if i.jugador_id == obj.creador_id:
                        perfil.puntos_acum -= 10
                        perfil.save()
                    else:
                        perfil.puntos_acum -= 5
                        perfil.save()
        super().save_model(request, obj, form, change)

admin.site.register(Partido, PartidoAdmin)
