from rest_framework import serializers
from .models import Invitacion
from partidos.serializers import PartidoSerializer, PartidoGetSerializer
from usuarios.serializers import PerfilSerializer

class InvitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitacion
        fields = ["id","usuario_invita","usuario_invitado","partido","fecha_hora_invitacion","estado"]

class InvitacionGetSerializer(serializers.ModelSerializer):
    partido = PartidoGetSerializer(many=False)
    usuario_invita = PerfilSerializer(many=False)
    class Meta:
        model = Invitacion
        fields = ["id","usuario_invita","usuario_invitado","partido","fecha_hora_invitacion","estado"]
