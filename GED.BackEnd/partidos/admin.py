from django.contrib import admin
from .models import Partido
from inscripciones.models import Inscripcion
from usuarios.models import Perfil
from django.utils import timezone

class PartidoAdmin(admin.ModelAdmin):
    exclude = ('fecha_hora_suspendido', 'fecha_hora_confirmado')

    def save_model(self, request, obj, form, change):
        if obj.confirmado == False and obj.fecha_hora_confirmado is None:
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
