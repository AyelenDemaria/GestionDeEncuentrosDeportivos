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
from django.contrib.auth import authenticate

class PartidoListApiView(APIView):
    # 1. List all
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        '''
        Lista de todos los partidos con fecha y hora mayor a la actual y cupo disponible
        '''
        partidos = Partido.objects.filter(suspendido=False)

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
        #fecha_hora_partido = datetime(request.data.get('fecha_hora'))
        #fecha_hora_part = datetime.strptime(request.data.get('fecha_hora'), '%Y-%m-%d %H:%M:%S')
        #fecha_hora_actual = timezone.localtime(timezone.now())
        #fecha_hora_partido = fecha_hora_part.astimezone(fecha_hora_actual.tzinfo)
        #if not (fecha_hora_partido <= fecha_hora_actual):
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
        #else:
        #    raise serializers.ValidationError('La fecha y hora del partido no puede ser menor a la actual')

    def put(self, request, *args, **kwargs):
        '''
        Updates the partido with given partido_id if exists
        '''

        pk = int(request.data["partido_id"])
        partido = Partido.objects.get(id = pk)
        if not partido:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'suspendido': True
        }
        serializer = PartidoSerializer(instance = partido, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """def delete(self, request, *args, **kwargs):
        pk = int(request.data["partido_id"])
        partido = partido.objects.get(id=pk)
        partido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""

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

class PartidoSemanaApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Valida si el usuario tiene partidos en los próximos 5 días
        '''
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)
        fecha_hora_actual = timezone.localtime(timezone.now())
        fecha_actual = fecha_hora_actual.date()
        partidos = Inscripcion.objects.filter(jugador_id = perfil.id, fecha_hora_baja__isnull=True, partido__fecha_hora__gt=fecha_hora_actual,  partido__suspendido=False)
        if partidos:
            for i in partidos:
                partido = Partido.objects.get(id=i.partido_id)
                fecha_hora_partido = timezone.localtime(partido.fecha_hora)
                fecha_partido = fecha_hora_partido.date()
                diferencia = datetime.strptime(str(fecha_partido),"%Y-%m-%d") - datetime.strptime(str(fecha_actual),"%Y-%m-%d")
                if diferencia.total_seconds() <= 432000:
                    print("hola")
                    return Response(1, status=status.HTTP_200_OK)
                    break
            return Response(0, status=status.HTTP_200_OK)
        else:
            return Response(0, status=status.HTTP_200_OK)


class InscritosByPartidoApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Lista de cada partido la cantidad de inscriptos
        '''
        partidos = Partido.objects.all()

        #fecha_hora_actual =  timezone.localtime(timezone.now())
        #partidos_mayor_hoy = []
        #partidos_mayor_hoy = Partido.objects.filter(timezone.localtime(fecha_hora)__gt = fecha_hora_actual)
        partidos_disp = []
        for i in partidos:
            #fecha_hora = timezone.localtime(i.fecha_hora)
            #if fecha_hora_actual < fecha_hora:
                #partidos_mayor_hoy.append(i)

        #for j in partidos_mayor_hoy:
            insc = Inscripcion.objects.filter(partido_id=i.id, fecha_hora_baja__isnull=True)
            cant_insc = insc.count()
            #if cant_insc < j.cant_jugadores:
            partidos_disp.append({'partido':i, 'cant_insc': cant_insc})
        serializer = InscriptosPartidoSerializer(partidos_disp, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
