from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import permissions
from .models import Invitacion
from inscripciones.models import Inscripcion
from .serializers import InvitacionSerializer, InvitacionGetSerializer
from inscripciones.serializers import InscripcionSerializer
from django.contrib.auth.models import User
from usuarios.models import Perfil
from django.shortcuts import get_object_or_404
from partidos.models import Partido
from django.utils import timezone
from datetime import datetime
# Create your views here.

class InvitacionListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]


    # 1. List all
    def get(self, request, *args, **kwargs):

        '''
        Lista de todas las invitaciones del usuario logueado
        '''
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        invitaciones = Invitacion.objects.filter(usuario_invitado = perfil.id, partido__suspendido=False).order_by("-partido__fecha_hora")
        serializer = InvitacionGetSerializer(invitaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create invitacion
        '''

        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        user_inv = request.data.get('usuario_invitado')
        perfil_inv = Perfil.objects.get(user_id=user_inv)


        data = {
            'usuario_invita': perfil.id,
            #'usuario_invitado': request.data.get('usuario_invitado'),
            'usuario_invitado': perfil_inv.id,
            'partido': request.data.get('partido'),
            'fecha_hora_invitacion': timezone.localtime(timezone.now()),

        }

        serializer = InvitacionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AceptarInvitacionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        '''
        Updates the inscripcion with given inscripcion_id if exists
        '''
        id_user = User.objects.get(username = request.user) #recupero usuario logueada
        perfil = Perfil.objects.get(user_id=id_user) #busco el perfil de ese usuario

        pk = int(request.data["invitacion_id"])
        invitacion = Invitacion.objects.get(id = pk)
        #busco si el usuario está ya inscripto a ese partido:
        insc_usuario = Inscripcion.objects.filter(jugador_id=perfil.id, partido_id=invitacion.partido_id)
        if not insc_usuario:
            #busco si el usuario está  inscripto a otro partido en esa fecha y hora:
            partido=Partido.objects.get(id=invitacion.partido_id)
            fecha_hora_partido = timezone.localtime(partido.fecha_hora)
            fecha_hora_actual = timezone.localtime(timezone.now())
            #partido_inscripto = Inscripcion.objects.filter(partido__fecha_hora=fecha_hora_partido, jugador_id=perfil.id, partido__suspendido=False)
            inscripciones = Inscripcion.objects.filter(partido__fecha_hora__gte=fecha_hora_actual,
                                                            fecha_hora_baja__isnull=True, jugador_id=perfil.id, partido__suspendido=False)
            partido_inscripto = []
            if inscripciones:
                for i in inscripciones:
                    fecha_deseada = fecha_hora_partido.date()
                    hora_deseada = fecha_hora_partido.time().strftime("%H:%M:%S")
                    fecha_hora_part = timezone.localtime(i.partido.fecha_hora)
                    fecha_part = fecha_hora_part.date()
                    hora_part = fecha_hora_part.time().strftime("%H:%M:%S")
                    if fecha_deseada == fecha_part:
                        diferencia = datetime.strptime(hora_deseada,"%H:%M:%S") - datetime.strptime(hora_part,"%H:%M:%S")
                        dif = abs(diferencia)
                        if dif.total_seconds()/3600 < 3:
                            partido_inscripto.append(i)

            if not partido_inscripto:
                data_invitacion = {
                    'estado': 'aceptada'
                }
                data_inscripcion = {
                        'jugador': perfil.id,
                        'fecha_hora_inscripcion': timezone.localtime(timezone.now()),
                        'partido': invitacion.partido_id

                    }
                serializer_inscripcion = InscripcionSerializer(data=data_inscripcion)
                if serializer_inscripcion.is_valid():
                        #print(serializer)
                        serializer_inscripcion.save()
                        perfil.puntos_acum += 5
                        perfil.save()
                        serializer_invitacion = InvitacionSerializer(instance = invitacion, data=data_invitacion, partial = True)
                        if serializer_invitacion.is_valid():
                            serializer_invitacion.save()
                            return Response(serializer_invitacion.data, status=status.HTTP_200_OK)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                data_invitacion = {
                    'estado': 'rechazada'
                }
                serializer_invitacion = InvitacionSerializer(instance = invitacion, data=data_invitacion, partial = True)
                if serializer_invitacion.is_valid():
                    serializer_invitacion.save()
                    raise serializers.ValidationError('Ya estas inscripto a otro partido en ese rango horario. La invitacion es rechazada')
                    return Response(serializer_invitacion.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data_invitacion = {
                'estado': 'rechazada'
            }
            serializer_invitacion = InvitacionSerializer(instance = invitacion, data=data_invitacion, partial = True)
            if serializer_invitacion.is_valid():
                serializer_invitacion.save()
                raise serializers.ValidationError('Ya estas inscripto al partido. La invitacion es rechazada')
                return Response(serializer_invitacion.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RechazarInvitacionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        '''
        Updates the inscripcion with given inscripcion_id if exists
        '''
        id_user = User.objects.get(username = request.user) #recupero usuario logueada
        perfil = Perfil.objects.get(user_id=id_user) #busco el perfil de ese usuario

        pk = int(request.data["invitacion_id"])
        invitacion = Invitacion.objects.get(id = pk)

        data_invitacion = {
            'estado': 'rechazada'
        }
        serializer = InvitacionSerializer(instance = invitacion, data=data_invitacion, partial = True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
