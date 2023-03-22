from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework import permissions
from .models import Perfil
from partidos.models import Partido
from inscripciones.models import Inscripcion
from vouchers.models import Voucher
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .serializers import PerfilSerializer,  UserSerializer, UserLoginSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.hashers import make_password


class PerfilListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        Lista de todos los usuarios
        '''

        usuarios = Perfil.objects.all()
        serializer = PerfilSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Registro usuario
        '''
        data_perfil = {
            'user': {
                'username': request.data.get('username'),
                'password': make_password(request.data.get('password')),
                'first_name': request.data.get('nombre'),
                'last_name': request.data.get('apellido'),
                'is_staff': 0
            },
            'documento': request.data.get('documento'),
            'telefono': request.data.get('telefono'),
            'fecha_nacimiento': request.data.get('fecha_nacimiento'),
            'sexo': request.data.get('sexo'),
            'puntos_acum': 0
        }

        serializer_perfil = PerfilSerializer(data=data_perfil)
        print('serializer perfil:',serializer_perfil)
        if serializer_perfil.is_valid():
            print('hola')
            serializer_perfil.save()
            print('hola 2')
            return Response(serializer_perfil.data, status=status.HTTP_201_CREATED)

        return Response(serializer_perfil.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        '''
        Updates the perfil with given perfil if exists
        '''

        id_user = User.objects.get(username = request.user) #recupero usuario logueada
        perfil = Perfil.objects.get(user_id=id_user) #busco el perfil de ese usuario

        serializer = PerfilSerializer(instance=perfil, data=request.data, partial = True)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CambioClaveAPIVIew(APIView):
    def put(self, request, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        print(request.data.get('password_1'))
        print(request.data.get('password_2'))
        if not (request.data.get('password_1') == None or request.data.get('password_2')== None):
            if request.data.get('password_1') == request.data.get('password_2'):
                usuario = User.objects.get(username = request.user)
                #usuario = User.objects.get(id=id_user)
                print("-------user:",usuario)
                usuario.password = make_password(request.data.get('password_1'))
                usuario.save()
                return Response("Clave actualizada con exito", status=status.HTTP_200_OK)
            else:
                raise serializers.ValidationError('Las contraseñas no coinciden')
        else:
            raise serializers.ValidationError('Debe completar todos los campos')


class UserLoginApiView(APIView):
    serializer_class = UserSerializer
    def post(self,request, *args, **kwargs):
        print("*", request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            #user = serializer.save()
            #serializer.save()
            user = serializer.save()
            data = {
                'username' : UserSerializer(user).data['username'],
                'password' : UserSerializer(user).data['password'],
            }

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDataAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)
        usuario = Perfil.objects.get(id=perfil.id)
        serializer = PerfilSerializer(usuario, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        #user = User.objects.get(request.data.get('username'))
        #print("usuario logueado:",user)
        logout(request)
        #print("luego del logout:", request.user)
        return Response('Se ha cerrado sesión', status=status.HTTP_200_OK)

class ReporteByUserApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        #partidos creados: busca los partidos donde creado_id sea el del usuario logueado
        partidos_creados = Partido.objects.filter(creador_id = perfil.id)
        #print("partidos creados:", partidos_creados)
        if partidos_creados:
            cant_partidos_creados = partidos_creados.count()
        else:
            print("no tiene partidos creados")
            cant_partidos_creados = 0

        #partidos a los que se unio: busca inscripciones donde el creado_id del partido NO sea el del usuario logueado
        inscripciones = Inscripcion.objects.filter(jugador_id = perfil.id)
        #print("inscripciones:", inscripciones)
        if inscripciones:
            if partidos_creados:
                part_no_creados = []
                for i in inscripciones:
                    if not i.partido in partidos_creados:
                        part_no_creados.append(i.partido)
                    """for j in partidos_creados:
                        if i.partido_id != j.id:
                            part_no_creados.append(j)"""
                #print("partidos no credos:",part_no_creados)
                if part_no_creados:
                    cant_unidos =  len(part_no_creados)
                else:
                     cant_unidos = 0
            else:
                cant_unidos = inscripciones.count()
        else:
            cant_unidos = 0

        #partidos jugados: busca inscripciones con fecha y hora de baja que NO esten en null en partidos ya pasados
        fecha_hora_actual =  timezone.localtime(timezone.now())
        jugados = Inscripcion.objects.filter(jugador_id = perfil.id, fecha_hora_baja__isnull=True, partido__fecha_hora__lt=fecha_hora_actual)
        if jugados:
            cant_jugados = jugados.count()
        else:
            cant_jugados = 0

        #partidos no jugados: busca inscripciones con fecha y hora de baja en null en partidos ya pasados
        no_jugados = Inscripcion.objects.filter(jugador_id = perfil.id, fecha_hora_baja__isnull=False, partido__fecha_hora__lt=fecha_hora_actual)
        if no_jugados:
            cant_no_jugados = no_jugados.count()
        else:
            cant_no_jugados = 0
        return Response([cant_partidos_creados, cant_unidos,cant_jugados,cant_no_jugados], status=status.HTTP_200_OK)


class PuntosUsertApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        '''
        Puntos del usuario logueado
        '''
        #permission_classes = [permissions.IsAuthenticated]
        id_user = User.objects.get(username = request.user)
        perfil = Perfil.objects.get(user_id=id_user)

        return Response(perfil.puntos_acum, status=status.HTTP_200_OK)


def reporte_usuarios(request):
    usuarios = Perfil.objects.all()
    resultado = []
    for k in usuarios:
        #partidos creados: busca los partidos donde creado_id sea el del usuario logueado
        partidos_creados = Partido.objects.filter(creador_id = k.id)
        if partidos_creados:
            cant_partidos_creados = partidos_creados.count()
        else:
            cant_partidos_creados = 0
        #partidos a los que se unio: busca inscripciones donde el creado_id del partido NO sea el del usuario logueado
        inscripciones = Inscripcion.objects.filter(jugador_id = k.id)
        #print("inscripciones:", inscripciones)
        if inscripciones:
            if partidos_creados:
                part_no_creados = []
                for i in inscripciones:
                    if not i.partido in partidos_creados:
                        part_no_creados.append(i.partido)
                    """for j in partidos_creados:
                        if i.partido_id != j.id:
                            print(j.id)
                            part_no_creados.append(j)"""
                if part_no_creados:
                    cant_unidos =  len(part_no_creados)
                else:
                     cant_unidos = 0
            else:
                cant_unidos = inscripciones.count()
        else:
            cant_unidos = 0
        #partidos jugados: busca inscripciones con fecha y hora de baja que NO esten en null en partidos ya pasados
        fecha_hora_actual =  timezone.localtime(timezone.now())
        jugados = Inscripcion.objects.filter(jugador_id = k.id, fecha_hora_baja__isnull=True, partido__fecha_hora__lt=fecha_hora_actual)
        if jugados:
            cant_jugados = jugados.count()
        else:
            cant_jugados = 0
        #partidos no jugados: busca inscripciones con fecha y hora de baja en null en partidos ya pasados
        no_jugados = Inscripcion.objects.filter(jugador_id = k.id, fecha_hora_baja__isnull=False, partido__fecha_hora__lt=fecha_hora_actual)
        if no_jugados:
            cant_no_jugados = no_jugados.count()
        else:
            cant_no_jugados = 0
        vouchers = Voucher.objects.filter(jugador_id = k.id)
        cant_vouchers = vouchers.count()
        resultado.append([k,k.puntos_acum,cant_partidos_creados, cant_unidos,cant_jugados,cant_no_jugados,cant_vouchers])
    resultado.sort(key = lambda resultado: resultado[1], reverse=True)
    return render(request, 'usuarios/reporte_usuarios.html', {'resultado': resultado})
