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
from django.utils import timezone
from datetime import datetime
from datetime import timedelta

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

    def post(self, request, *args, **kwargs):
        '''
        Create voucher
        '''

        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)
        fecha_hora_actual= timezone.localtime(timezone.now())
        fecha_actual = fecha_hora_actual.date()
        fecha_vencimiento = fecha_actual + timedelta(days=30)
        print("fecha actual:",fecha_actual)
        print("fecha_vencimiento:",fecha_vencimiento)

        data = {
            'jugador': perfil.id,
            'cancha': request.data.get('cancha_id'),
            'fecha_emision': fecha_actual,
            'fecha_vencimiento': fecha_vencimiento,

        }

        serializer = VoucherSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            perfil.puntos_acum -= 30
            perfil.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        '''
        Updates the voucher with given voucher_id if exists
        '''
        id_user = User.objects.get(username = request.user) #recupero usuario logueada
        perfil = Perfil.objects.get(user_id=id_user) #busco el perfil de ese usuario
        #pk = self.kwargs.get('pk') #obtengo la pk de la url que es la inscripcion
        pk = int(request.data["voucher_id"])
        voucher = Voucher.objects.get(id = pk) 
        if not voucher:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'fecha_canje': timezone.localtime(timezone.now()).date()
        }
        serializer = VoucherSerializer(instance = voucher, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
