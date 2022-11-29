from rest_framework import serializers
from .models import Inscripcion

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = ["jugador","partido","fecha_hora_inscripcion","fecha_hora_baja"]
