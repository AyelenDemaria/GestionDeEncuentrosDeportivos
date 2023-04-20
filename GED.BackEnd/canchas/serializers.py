from rest_framework import serializers
from .models import Cancha, CanchaPrecio
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
        fields = ["id","nombre","direccion","deporte"]

class CanchaPrecioSerializer(serializers.ModelSerializer):
    cancha = CanchaGetSerializer(many=False)
    class Meta:
        model = CanchaPrecio
        fields = ["id","cancha","fecha","abono_mensual","valor_uso", "valor_referi"]
