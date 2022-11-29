from django.db import models
from django.conf import settings
from canchas.models import Cancha
from usuarios.models import Perfil
from tipos_partidos.models import Tipo_partido

# Create your models here.
class Partido(models.Model):
    fecha_hora = models.DateTimeField(null=False)
    cant_jugadores = models.BigIntegerField()
    tipo_partido = models.ForeignKey(Tipo_partido, on_delete=models.CASCADE)
    creador = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha_hora) + '-' + str(self.cancha) + str(self.tipo_partido)
