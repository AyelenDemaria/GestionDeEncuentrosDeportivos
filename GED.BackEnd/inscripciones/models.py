from django.db import models
from django.conf import settings
from partidos.models import Partido
from usuarios.models import Perfil
from django.contrib import admin

# Create your models here.
class Inscripcion(models.Model):
    jugador = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    fecha_hora_inscripcion = models.DateTimeField(null=False)
    fecha_hora_baja = models.DateTimeField(blank=True, null=True)
    notificado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.jugador) + ' / ' + str(self.partido)

class InscripcionAdmin(admin.ModelAdmin):
    fields =  ['id', 'jugador', 'cant_jugadores', 'partido', 'fecha_hora_inscripcion', 'fecha_hora_baja']
