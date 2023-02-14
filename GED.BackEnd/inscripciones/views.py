from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Inscripcion
from .serializers import InscripcionSerializer
from django.contrib.auth.models import User
from usuarios.models import Perfil
from django.shortcuts import get_object_or_404
from partidos.models import Partido
from django.utils import timezone
from datetime import datetime


class InscripcionListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]


    # 1. List all
    def get(self, request, *args, **kwargs):

        '''
        Lista de todas las inscripciones
        '''
        inscripciones = Inscripcion.objects.all()
        serializer = InscripcionSerializer(inscripciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create inscripcion
        '''
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)
        pk = int(request.data["partido_id"])
        #print(request.data)
        #pk = self.kwargs.get('pk')
        partido = get_object_or_404(Partido, pk=pk)
        fecha_partido = partido.fecha_hora.date()

        #print(fecha_partido)
        data = {
            'jugador': perfil.id,
            'fecha_hora_inscripcion': timezone.localtime(timezone.now()),
            'partido': pk

        }
        serializer = InscripcionSerializer(data=data)
        if serializer.is_valid():
            #print(serializer)
            serializer.save()
            perfil.puntos_acum += 5
            perfil.save()
            print(perfil.puntos_acum)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        '''
        Updates the inscripcion with given inscripcion_id if exists
        '''
        id_user = User.objects.get(username = request.user) #recupero usuario logueada
        perfil = Perfil.objects.get(user_id=id_user) #busco el perfil de ese usuario
        #pk = self.kwargs.get('pk') #obtengo la pk de la url que es la inscripcion
        pk = int(request.data["inscripcion_id"])
        inscripcion = Inscripcion.objects.get(id = pk)
        #inscripcion = self.get_object(pk, perfil.id)
        if not inscripcion:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'fecha_hora_baja': timezone.localtime(timezone.now())
        }
        serializer = InscripcionSerializer(instance = inscripcion, data=data, partial = True)
        if serializer.is_valid():
            fecha_hora_actual = timezone.localtime(timezone.now())
            fecha_actual = fecha_hora_actual.date()
            hora_actual = fecha_hora_actual.time().strftime("%H:%M:%S")
            partido = Partido.objects.get(id = inscripcion.partido_id)
            fecha_hora_partido = timezone.localtime(partido.fecha_hora)
            fecha_partido = fecha_hora_partido.date()
            hora_partido = fecha_hora_partido.time().strftime("%H:%M:%S")
            print("fecha_partido:", fecha_partido)
            print("hora_partido:", hora_partido)
            print("fecha_actual:", fecha_actual)
            print("hora actual:",hora_actual)


            if fecha_actual == fecha_partido:
                diferencia = datetime.strptime(hora_actual,"%H:%M:%S") - datetime.strptime(hora_partido,"%H:%M:%S")

                print("dif:", diferencia)
                #hs_actual = hora_actual.hour()
                #print(hs_actual)
                #diferencia_hs = datetime.timedelta(hs_actual)
                #print(diferencia_hs)
                if diferencia.total_seconds()/3600 < 5:
                    perfil.puntos_acum -= 15
                    perfil.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InscripcionByUserApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        Lista de todas las inscripciones de un usuario logueado
        '''
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        #pk = self.kwargs.get('pk')
        inscripciones = Inscripcion.objects.filter(jugador_id = perfil.id)
        serializer = InscripcionSerializer(inscripciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
