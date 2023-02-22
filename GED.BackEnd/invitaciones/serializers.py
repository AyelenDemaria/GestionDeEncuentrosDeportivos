from rest_framework import serializers
from .models import Invitacion

class InvitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitacion
        fields = ["usuario_invita","usuario_invitado","partido","fecha_hora_invitacion","estado"]
