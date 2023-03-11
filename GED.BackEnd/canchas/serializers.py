from rest_framework import serializers
from .models import Cancha
from deportes.models import Deporte
from deportes.serializers import DeporteSerializer

"""class DeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deporte
        fields = ["descripcion"]"""

class CanchaSerializer(serializers.ModelSerializer):
    deporte = DeporteSerializer(many=False)
    class Meta:
        model = Cancha
        fields = ["id","nombre","direccion","deporte"]
