from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import permissions
from .models import Invitacion
from inscripciones.models import Inscripcion
from .serializers import InvitacionSerializer
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

        invitaciones = Invitacion.objects.filter(usuario_invitado = perfil.id)
        serializer = InvitacionSerializer(invitaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create invitacion
        '''

        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        data = {
            'usuario_invita': perfil.id,
            'usuario_invitado': request.data.get('usuario_invitado'),
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

        data_invitacion = {
            'estado': 'aceptada'
        }
        serializer = InvitacionSerializer(instance = invitacion, data=data_invitacion, partial = True)
        if serializer.is_valid():
            serializer.save()
            insc_usuario = Inscripcion.objects.get(jugador_id=perfil.id, partido_id=invitacion.partido_id)
            if insc_usuario is None:
                data_inscripcion = {
                        'jugador': perfil.id,
                        'fecha_hora_inscripcion': timezone.localtime(timezone.now()),
                        'partido': invitacion.partido_id

                    }

                serializer = InscripcionSerializer(data=data_inscripcion)
                if serializer.is_valid():
                        #print(serializer)
                        serializer.save()
                        perfil.puntos_acum += 5
                        perfil.save()

            else:
                raise serializers.ValidationError('Ya estas inscripto al partido')
            return Response(serializer.data, status=status.HTTP_200_OK)
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
