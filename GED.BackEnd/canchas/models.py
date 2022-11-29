from django.db import models
from django.conf import settings
from deportes.models import Deporte

# Create your models here.
class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + '-' + self.direccion
