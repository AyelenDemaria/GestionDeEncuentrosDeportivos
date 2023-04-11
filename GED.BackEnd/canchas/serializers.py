from rest_framework import serializers
from .models import Cancha
from deportes.models import Deporte
from deportes.serializers import DeporteSerializer

class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = ["id","nombre","direccion","deporte"]

class CanchaGetSerializer(serializers.ModelSerializer):
    deporte = DeporteSerializer(many=False)
    class Meta:
        model = Cancha
        fields = ["id","nombre","direccion","deporte", "valor_uso", "valor_referi"]
