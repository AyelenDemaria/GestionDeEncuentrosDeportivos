from rest_framework import serializers
from .models import Voucher

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ["fecha_canje", "fecha_emision", "fecha_vencimiento", "jugador", "cancha"]
