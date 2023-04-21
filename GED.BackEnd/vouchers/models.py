from django.db import models
from django.conf import settings
from canchas.models import Cancha, CanchaPrecio
from usuarios.models import Perfil
from django.contrib import admin

# Create your models here.
class Voucher(models.Model):
    fecha_canje = models.DateField(null=True)
    fecha_emision = models.DateField(null=False)
    fecha_vencimiento = models.DateField(null=False)
    jugador = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    cancha = models.ForeignKey(CanchaPrecio, on_delete=models.CASCADE)
    codigo = models.BigIntegerField(null=True)

    def __str__(self):
        return str(self.jugador) + '-' + str(self.cancha) + str(self.fecha_emision)

class VoucherAdmin(admin.ModelAdmin):
    fields =  ['id', 'fecha_canje', 'fecha_emision', 'fecha_vencimiento', 'jugador','cancha','codigo']
