from django.db import models
from usuarios.models import Perfil
from partidos.models import Partido


# Create your models here.
class Invitacion(models.Model):
    usuario_invitado = models.ForeignKey(Perfil,related_name='%(class)s_requests_invitado', on_delete=models.CASCADE)
    usuario_invita = models.ForeignKey(Perfil, related_name='%(class)s_requests_invita', on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    fecha_hora_invitacion =  models.DateTimeField(null=False)
    estado = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return  str(self.usuario_invita) +  '-' + str(self.partido) +  '-' + str(self.usuario_invitado)
