from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Partido
from inscripciones.models import Inscripcion
from .serializers import PartidoSerializer, PartidoGetSerializer, InscriptosPartidoSerializer
from inscripciones.serializers import InscripcionSerializer
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from usuarios.models import Perfil
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers

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
        partidos_mayor_hoy = []
        #partidos_mayor_hoy = Partido.objects.filter(timezone.localtime(fecha_hora)__gt = fecha_hora_actual)
        for i in partidos:
            fecha_hora = timezone.localtime(i.fecha_hora)
            if fecha_hora_actual < fecha_hora:
                partidos_mayor_hoy.append(i)
        partidos_disp = []
        for j in partidos_mayor_hoy:
            insc = Inscripcion.objects.filter(partido_id=j.id, fecha_hora_baja__isnull=True)
            cant_insc = insc.count()
            if cant_insc < j.cant_jugadores:
                partidos_disp.append(j)
        serializer = PartidoGetSerializer(partidos_disp, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create partido
        '''

        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)
        print("fecha_hora:",request.data.get('fecha_hora'))
        print("cancha:",request.data.get('cancha'))
        partido_existente = Partido.objects.filter(fecha_hora=request.data.get('fecha_hora'),
                                            cancha=request.data.get('cancha'))
        if not partido_existente:
            inscripcion_existente = Inscripcion.objects.filter(partido__fecha_hora=request.data.get('fecha_hora'),
                                                                fecha_hora_baja__isnull=True, jugador_id=perfil.id)
            if not inscripcion_existente:
                data = {
                    'fecha_hora': request.data.get('fecha_hora'),
                    'cant_jugadores': request.data.get('cant_jugadores'),
                    'tipo_partido': request.data.get('tipo_partido'),
                    'cancha': request.data.get('cancha'),
                    'creador': perfil.id
                }
                serializer_partido = PartidoSerializer(data=data)
                if serializer_partido.is_valid():
                    serializer_partido.save()
                    perfil.puntos_acum += 10
                    perfil.save()
                    partido_creado = Partido.objects.get(fecha_hora=request.data.get('fecha_hora'),
                                                        cancha=request.data.get('cancha'),
                                                        creador=perfil.id)
                    data_inscripcion = {
                            'jugador': perfil.id,
                            'fecha_hora_inscripcion': timezone.localtime(timezone.now()),
                            'partido': partido_creado.id
                        }
                    serializer_inscripcion = InscripcionSerializer(data=data_inscripcion)
                    if serializer_inscripcion.is_valid():
                            serializer_inscripcion.save()
                    return Response(serializer_partido.data, status=status.HTTP_201_CREATED)
                return Response(serializer_partido.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise serializers.ValidationError('Ya estas inscripto a otro partido en esa fecha y hora')
        else:
            raise serializers.ValidationError('Ya existe un partido para esa fecha y hora en esa cancha')


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
        serializer = PartidoGetSerializer(partidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InscritosByPartidoApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Lista de cada partido la cantidad de inscriptos
        '''
        partidos = Partido.objects.all()

        fecha_hora_actual =  timezone.localtime(timezone.now())
        partidos_mayor_hoy = []
        #partidos_mayor_hoy = Partido.objects.filter(timezone.localtime(fecha_hora)__gt = fecha_hora_actual)
        for i in partidos:
            fecha_hora = timezone.localtime(i.fecha_hora)
            if fecha_hora_actual < fecha_hora:
                partidos_mayor_hoy.append(i)
        partidos_disp = []
        for j in partidos_mayor_hoy:
            insc = Inscripcion.objects.filter(partido_id=j.id, fecha_hora_baja__isnull=True)
            cant_insc = insc.count()
            if cant_insc < j.cant_jugadores:
                partidos_disp.append({'partido':j, 'cant_insc': cant_insc})
        serializer = InscriptosPartidoSerializer(partidos_disp, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
