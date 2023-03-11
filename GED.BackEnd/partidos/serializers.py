from rest_framework import serializers
from .models import Partido, InscriptosPartido
from canchas.serializers import  CanchaSerializer
from tipos_partidos.serializers import Tipo_partidoSerializer

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = ["id","fecha_hora","cant_jugadores","tipo_partido","cancha","creador"]

class PartidoGetSerializer(serializers.ModelSerializer):
    cancha = CanchaSerializer (many=False)
    tipo_partido = Tipo_partidoSerializer (many=False)
    class Meta:
        model = Partido
        fields = ["id","fecha_hora","cant_jugadores","tipo_partido","cancha","creador"]

class InscriptosPartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscriptosPartido
        fields = ["partido", "cant_insc"]
