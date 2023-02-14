from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Voucher
from usuarios.models import Perfil
from django.contrib.auth.models import User
from .serializers import VoucherSerializer

class  VoucherListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        Lista de todos los vouchers de un usuario logueado
        '''
        #vouchers = Voucher.objects.all()
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)
        vouchers = Voucher.objects.filter(jugador = perfil.id)
        serializer = VoucherSerializer(vouchers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
