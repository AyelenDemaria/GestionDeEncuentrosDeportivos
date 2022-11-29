from rest_framework import serializers
from .models import Tipo_partido

class Tipo_partidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_partido
        fields = ["descripcion"]
