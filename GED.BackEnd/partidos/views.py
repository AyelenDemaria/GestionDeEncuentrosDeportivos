from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Partido
from inscripciones.models import Inscripcion
from .serializers import PartidoSerializer
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from usuarios.models import Perfil
from django.shortcuts import get_object_or_404
from django.db.models import Q

class PartidoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        Lista de todos los partidos con fecha y hora mayor a la actual y cupo disponible
        '''
        partidos = Partido.objects.all()
        fecha_hora_actual =  timezone.localtime(timezone.now())
        print(fecha_hora_actual)
        partidos_mayor_hoy = []
        #partidos_mayor_hoy = Partido.objects.filter(timezone.localtime(fecha_hora)__gt = fecha_hora_actual)
        for i in partidos:
            fecha_hora = timezone.localtime(i.fecha_hora)
            print("fecha_hora_partido: ",fecha_hora)
            if fecha_hora_actual < fecha_hora:
                print("hola")
                partidos_mayor_hoy.append(i)
        print("partidos fecha mayor:", partidos_mayor_hoy)
        partidos_disp = []
        for j in partidos_mayor_hoy:
            insc = Inscripcion.objects.filter(partido_id=j.id, fecha_hora_baja__isnull=True)
            cant_insc = insc.count()
            print(j, cant_insc)
            if cant_insc < j.cant_jugadores:
                partidos_disp.append(j)
        serializer = PartidoSerializer(partidos_disp, many=True)
        print(serializer)
        """partidos_insc = []
        for j in partidos_disp:
            inscrip = Inscripcion.objects.filter(partido_id=j.id, fecha_hora_baja__isnull=True)
            cant_inscripciones = inscrip.count()
            partidos_insc.append([j,cant_inscripciones])"""
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create partido
        '''

        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        data = {
            'fecha_hora': request.data.get('fecha_hora'),
            'cant_jugadores': request.data.get('cant_jugadores'),
            'tipo_partido': request.data.get('tipo_partido'),
            'cancha': request.data.get('cancha'),
            'creador': perfil.id
        }

        serializer = PartidoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            perfil.puntos_acum += 10
            perfil.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartidoByUserApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Lista de todos los partidos creados por el usuario logueado
        '''
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        #pk = self.kwargs.get('pk')
        partidos = Partido.objects.filter(creador_id = perfil.id)
        serializer = PartidoSerializer(partidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
