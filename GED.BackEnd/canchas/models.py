from django.db import models
from django.conf import settings
from deportes.models import Deporte

# Create your models here.
class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    valor_uso = models.DecimalField(max_digits = 6, decimal_places = 2, default=1000.00)
    valor_referi = models.DecimalField(max_digits = 6, decimal_places = 2, default=0.00)
    abono_mensual = models.DecimalField(max_digits = 6, decimal_places = 2, default=1500.00)

    def __str__(self):
        return self.nombre + ' / ' + self.direccion + ' / Deporte: ' + self.deporte.descripcion
