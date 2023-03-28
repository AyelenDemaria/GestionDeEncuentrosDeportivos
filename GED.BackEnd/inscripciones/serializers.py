from rest_framework import serializers
from .models import Inscripcion
from partidos.serializers import PartidoGetSerializer
from usuarios.serializers import PerfilSerializer

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = ["id","jugador","partido","fecha_hora_inscripcion","fecha_hora_baja"]

class InscripcionGetSerializer(serializers.ModelSerializer):
    partido = PartidoGetSerializer(many=False)
    jugador = PerfilSerializer(many=False)
    class Meta:
        model = Inscripcion
        fields = ["id","jugador","partido","fecha_hora_inscripcion","fecha_hora_baja"]
