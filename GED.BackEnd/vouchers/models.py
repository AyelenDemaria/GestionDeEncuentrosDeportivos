from django.db import models
from django.conf import settings
from canchas.models import Cancha
from usuarios.models import Perfil

# Create your models here.
class Voucher(models.Model):
    fecha_canje = models.DateField(null=False)
    fecha_emision = models.DateField(null=False)
    fecha_vencimiento = models.DateField(null=False)
    jugador = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.jugador) + '-' + str(self.cancha) + str(self.fecha_emision)
