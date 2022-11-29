from django.db import models
from django.conf import settings
from partidos.models import Partido
from usuarios.models import Perfil


# Create your models here.
class Inscripciones(models.Model):
    jugador = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    fecha_hora_inscripcion = models.DateTimeField(null=False)
    fecha_hora_baja = models.DateTimeField(null=False)

    def __str__(self):
        return str(self.jugador) + '-' + str(self.partido)
