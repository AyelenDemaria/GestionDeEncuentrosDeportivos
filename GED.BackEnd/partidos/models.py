from django.db import models
from django.conf import settings
from canchas.models import CanchaPrecio
from usuarios.models import Perfil
from tipos_partidos.models import Tipo_partido
from django.contrib import admin

# Create your models here.
class Partido(models.Model):
    fecha_hora = models.DateTimeField(null=False)
    cant_jugadores = models.BigIntegerField()
    tipo_partido = models.ForeignKey(Tipo_partido, on_delete=models.CASCADE)
    creador = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    cancha = models.ForeignKey(CanchaPrecio, on_delete=models.CASCADE)
    suspendido = models.BooleanField(default=False)
    fecha_hora_suspendido = models.DateTimeField(null=True)
    confirmado =  models.BooleanField(default=True)
    fecha_hora_confirmado = models.DateTimeField(null=True)


    def __str__(self):
        return str(self.fecha_hora) + ' - ' + str(self.cancha) + ' - ' + str(self.tipo_partido)

class PartidoAdmin(admin.ModelAdmin):
    fields =  ['id', 'fecha_hora', 'cant_jugadores', 'tipo_partido', 'creador', 'cancha', 'suspendido', 'fecha_hora_suspendido','confirmado','fecha_hora_confirmado']

class InscriptosPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    cant_insc = models.BigIntegerField()

    def __str__(self):
        return str(self.partido) + ' - ' + str(self.cant_insc)
