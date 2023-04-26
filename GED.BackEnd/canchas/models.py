from django.db import models
from django.conf import settings
from deportes.models import Deporte
from django.contrib import admin
from datetime import date

# Create your models here.
class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(null=True, default=date.today)
    fecha_baja = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.nombre + ' / ' + self.direccion + ' / Deporte: ' + self.deporte.descripcion

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

class CanchaAdmin(admin.ModelAdmin):
    fields =  ['id', 'nombre', 'direccion', 'deporte']


class CanchaPrecio(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    valor_uso = models.DecimalField(max_digits = 10, decimal_places = 2, default=1000.00)
    valor_referi = models.DecimalField(max_digits = 10, decimal_places = 2, default=0.00)
    abono_mensual = models.DecimalField(max_digits = 10, decimal_places = 2, default=1500.00)
    fecha = models.DateField(null=True)

    def __str__(self):
        return self.cancha.nombre + ' / ' + str(self.fecha) + ' / valor uso: ' + str(self.valor_uso) + ' / valor referi:' + str(self.valor_referi) + ' / abono:' + str(self.abono_mensual)

class CanchaPrecioAdmin(admin.ModelAdmin):
    fields =  ['id', 'cancha', 'fecha','abono_mensual', 'valor_uso', 'valor_referi']
