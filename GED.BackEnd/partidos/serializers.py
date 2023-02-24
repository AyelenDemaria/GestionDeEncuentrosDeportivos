from rest_framework import serializers
from .models import Partido, InscriptosPartido

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = ["fecha_hora","cant_jugadores","tipo_partido","cancha","creador"]

class InscriptosPartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscriptosPartido
        fields = ["partido", "cant_insc"]
