from rest_framework import serializers
from .models import Inscripcion
from partidos.serializers import PartidoSerializer
from usuarios.serializers import PerfilSerializer

class InscripcionSerializer(serializers.ModelSerializer):
    partido = PartidoSerializer(many=False)
    jugador = PerfilSerializer(many=False)
    class Meta:
        model = Inscripcion
        fields = ["jugador","partido","fecha_hora_inscripcion","fecha_hora_baja"]
