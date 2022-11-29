from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    documento = models.CharField(max_length=8)
    telefono = models.CharField(max_length=10)
    fecha_nacimiento =  models.DateField(null=False)
    sexo = models.CharField(max_length=9)
    puntos_acum = models.BigIntegerField()

    def __str__(self):
        return self.documento
