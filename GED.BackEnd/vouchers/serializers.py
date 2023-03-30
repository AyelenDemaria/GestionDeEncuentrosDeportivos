from rest_framework import serializers
from .models import Voucher
from canchas.serializers import CanchaSerializer,  CanchaGetSerializer
from usuarios.serializers import PerfilSerializer


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ["id","fecha_canje", "fecha_emision", "fecha_vencimiento", "jugador", "cancha"]

class VoucherGetSerializer(serializers.ModelSerializer):
    cancha = CanchaGetSerializer(many=False)
    jugador = PerfilSerializer(many=False)
    class Meta:
        model = Voucher
        fields = ["id","fecha_canje", "fecha_emision", "fecha_vencimiento", "jugador", "cancha"]
