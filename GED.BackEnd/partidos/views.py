from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Partido
from canchas.models import Cancha,CanchaPrecio
from inscripciones.models import Inscripcion
from deportes.models import Deporte
from tipos_partidos.models import Tipo_partido
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
from canchas.forms import ReporteMesAnio

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
        cancha_id = request.data.get('cancha')
        cancha_r = Cancha.objects.get(id=cancha_id)
        fecha_hora_actual = timezone.localtime(timezone.now())
        fecha_actual = fecha_hora_actual.date()
        cancha_precio = CanchaPrecio.objects.filter(cancha = cancha_r, fecha__lte=fecha_actual).latest('fecha')
        """partido_existente = Partido.objects.filter(fecha_hora=request.data.get('fecha_hora'),
                                            cancha__cancha=cancha_r,suspendido=False)"""
        partidos_existentes = Partido.objects.filter(fecha_hora__gte=fecha_hora_actual,
                                            cancha__cancha=cancha_r,suspendido=False)
        partido_existente = []
        if partidos_existentes:
            for p in partidos_existentes:
                fecha_hora_ingresada = datetime.strptime(request.data.get('fecha_hora'),'%Y-%m-%d %H:%M:%S')
                fecha_ingresada = fecha_hora_ingresada.date()
                hora_ingresada = fecha_hora_ingresada.time().strftime("%H:%M:%S")
                fecha_hora_partido = timezone.localtime(p.fecha_hora)
                fecha_partido = fecha_hora_partido.date()
                hora_partido = fecha_hora_partido.time().strftime("%H:%M:%S")
                if fecha_ingresada == fecha_partido:
                    diferencia = datetime.strptime(hora_ingresada,"%H:%M:%S") - datetime.strptime(hora_partido,"%H:%M:%S")
                    dif = abs(diferencia)
                    if dif.total_seconds()/3600 < 3:
                        partido_existente.append(p)

        if not partido_existente:
            """inscripciones = Inscripcion.objects.filter(partido__fecha_hora=request.data.get('fecha_hora'),
                                                            fecha_hora_baja__isnull=True, jugador_id=perfil.id, partido__suspendido=False)"""
            inscripciones = Inscripcion.objects.filter(partido__fecha_hora__gte=fecha_hora_actual,
                                                            fecha_hora_baja__isnull=True, jugador_id=perfil.id, partido__suspendido=False)
            inscripcion_existente = []
            if inscripciones:
                for i in inscripciones:
                    fecha_hora_ingresada = datetime.strptime(request.data.get('fecha_hora'),'%Y-%m-%d %H:%M:%S')
                    fecha_ingresada = fecha_hora_ingresada.date()
                    hora_ingresada = fecha_hora_ingresada.time().strftime("%H:%M:%S")
                    fecha_hora_partido = timezone.localtime(i.partido.fecha_hora)
                    fecha_partido = fecha_hora_partido.date()
                    hora_partido = fecha_hora_partido.time().strftime("%H:%M:%S")
                    if fecha_ingresada == fecha_partido:
                        diferencia = datetime.strptime(hora_ingresada,"%H:%M:%S") - datetime.strptime(hora_partido,"%H:%M:%S")
                        dif = abs(diferencia)
                        if dif.total_seconds()/3600 < 3:
                            inscripcion_existente.append(i)

            if not inscripcion_existente:
                data = {
                    'fecha_hora': request.data.get('fecha_hora'),
                    'cant_jugadores': request.data.get('cant_jugadores'),
                    'tipo_partido': request.data.get('tipo_partido'),
                    'cancha': cancha_precio.id,
                    'creador': perfil.id
                }
                serializer_partido = PartidoSerializer(data=data)
                if serializer_partido.is_valid():
                    serializer_partido.save()
                    perfil.puntos_acum += 10
                    perfil.save()
                    partido_creado = Partido.objects.get(fecha_hora=request.data.get('fecha_hora'),
                                                        cancha__cancha=cancha_r,
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
                raise serializers.ValidationError('Ya estas inscripto a otro partido en ese rango horario')
        else:
            raise serializers.ValidationError('Ya existe un partido en ese rango horario en esa cancha')
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


def reporte_partidos_deportes(request):
    if request.method == "POST":
        form = ReporteMesAnio(request.POST)
        if form.is_valid():
            mes_actual = int(form.cleaned_data["mes"])
            anio_actual = int(form.cleaned_data["anio"])
            deportes = Deporte.objects.all()
            resultado = []
            for d in deportes:
                #partidos = Partido.objects.filter(cancha__deporte=d, fecha_hora__date__year=anio_actual, fecha_hora__date__month=mes_actual)
                partidos_totales = []
                partidos_jugados = []
                partidos_suspendidos = []
                partidos_noconfirmados = []
                #partidos = Partido.objects.filter(cancha__cancha=c, fecha_hora__year=anio_actual, fecha_hora__month=mes_actual)
                partidos_j = Partido.objects.filter(cancha__cancha__deporte=d, confirmado=1, suspendido=0)
                partidos_t = Partido.objects.filter(cancha__cancha__deporte=d)
                partidos_s = Partido.objects.filter(cancha__cancha__deporte=d,confirmado=1, suspendido=1 )
                partidos_nc = Partido.objects.filter(cancha__cancha__deporte=d, confirmado=0, suspendido=0)
                for t in partidos_t:
                    anio = int(t.fecha_hora.strftime('%Y'))
                    mes = int(t.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_totales.append(t)
                cant_partidos_totales = len(partidos_totales)
                for j in partidos_j:
                    anio = int(j.fecha_hora.strftime('%Y'))
                    mes = int(j.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_jugados.append(j)
                cant_partidos_jugados = len(partidos_jugados)
                for s in partidos_s:
                    anio = int(s.fecha_hora.strftime('%Y'))
                    mes = int(s.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_suspendidos.append(s)
                cant_partidos_suspendidos = len(partidos_suspendidos)
                for nc in partidos_nc:
                    anio = int(nc.fecha_hora.strftime('%Y'))
                    mes = int(nc.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_noconfirmados.append(nc)
                cant_partidos_noconfirmados = len(partidos_noconfirmados)
                resultado.append([d,cant_partidos_totales, cant_partidos_jugados, cant_partidos_suspendidos, cant_partidos_noconfirmados])
            resultado.sort(key = lambda resultado: resultado[2], reverse=True)
            return render(request, 'partidos/reporte_partidos_deportes.html', {'form': form, 'resultado': resultado})
    else:
        form = ReporteMesAnio()
    return render(request, 'partidos/reporte_partidos_deportes.html', {'form': form})

def reporte_partidos_canchas(request):
    if request.method == "POST":
        form = ReporteMesAnio(request.POST)
        if form.is_valid():
            mes_actual = int(form.cleaned_data["mes"])
            anio_actual = int(form.cleaned_data["anio"])
            canchas = Cancha.objects.all()
            resultado = []
            canchas_vigentes = []
            for cancha in canchas:
                mes_ingreso = int(cancha.fecha_ingreso.strftime('%m'))
                anio_ingreso = int(cancha.fecha_ingreso.strftime('%Y'))
                if mes_ingreso <= mes_actual and anio_ingreso <= anio_actual:
                    if cancha.fecha_baja is not None:
                        mes_baja = int(cancha.fecha_baja.strftime('%m'))
                        anio_baja = int(cancha.fecha_baja.strftime('%Y'))
                        if mes_actual < mes_baja and anio_actual <= anio_baja:
                            canchas_vigentes.append(cancha)
                    else:
                        canchas_vigentes.append(cancha)
            for c in canchas_vigentes:
                partidos_jugados = []
                partidos_totales = []
                partidos_suspendidos = []
                partidos_noconfirmados = []
                #partidos = Partido.objects.filter(cancha__cancha=c, fecha_hora__year=anio_actual, fecha_hora__month=mes_actual)
                partidos_j = Partido.objects.filter(cancha__cancha=c, confirmado=1, suspendido=0)
                partidos_t = Partido.objects.filter(cancha__cancha=c)
                partidos_s = Partido.objects.filter(cancha__cancha=c,confirmado=1, suspendido=1 )
                partidos_nc = Partido.objects.filter(cancha__cancha=c, confirmado=0, suspendido=0)
                for j in partidos_j:
                    anio = int(j.fecha_hora.strftime('%Y'))
                    mes = int(j.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_jugados.append(j)
                cant_partidos_jugados = len(partidos_jugados)
                for t in partidos_t:
                    anio = int(t.fecha_hora.strftime('%Y'))
                    mes = int(t.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_totales.append(t)
                cant_partidos_totales = len(partidos_totales)
                for s in partidos_s:
                    anio = int(s.fecha_hora.strftime('%Y'))
                    mes = int(s.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_suspendidos.append(s)
                cant_partidos_suspendidos = len(partidos_suspendidos)
                for nc in partidos_nc:
                    anio = int(nc.fecha_hora.strftime('%Y'))
                    mes = int(nc.fecha_hora.strftime('%m'))
                    if anio == anio_actual and mes == mes_actual:
                        partidos_noconfirmados.append(nc)
                cant_partidos_noconfirmados = len(partidos_noconfirmados)
                resultado.append([c, cant_partidos_totales, cant_partidos_jugados, cant_partidos_suspendidos, cant_partidos_noconfirmados])
            resultado.sort(key = lambda resultado: resultado[2], reverse=True)
            return render(request, 'partidos/reporte_partidos_canchas.html', {'form': form, 'resultado': resultado})
    else:
        form = ReporteMesAnio()
    return render(request, 'partidos/reporte_partidos_canchas.html', {'form': form})

def reporte_partidos_tipos(request):
    if request.method == "POST":
        form = ReporteMesAnio(request.POST)
        if form.is_valid():
            mes_actual = int(form.cleaned_data["mes"])
            anio_actual = int(form.cleaned_data["anio"])
            tipos_partidos = Tipo_partido.objects.all()
            resultado = []
            for c in tipos_partidos:
                partidos_jugados = []
                partidos_totales = []
                partidos_suspendidos = []
                partidos_noconfirmados = []
                cant_partidos_jugados = 0
                cant_partidos_suspendidos = 0
                cant_partidos_totales = 0
                cant_partidos_noconfirmados = 0
                #partidos = Partido.objects.filter(cancha__cancha=c, fecha_hora__year=anio_actual, fecha_hora__month=mes_actual)
                partidos_j = Partido.objects.filter(tipo_partido=c, confirmado=1, suspendido=0)
                partidos_t = Partido.objects.filter(tipo_partido=c)
                print("------ partidos",partidos_t)
                partidos_s = Partido.objects.filter(tipo_partido=c,confirmado=1, suspendido=1 )
                partidos_nc = Partido.objects.filter(tipo_partido=c, confirmado=0, suspendido=0)
                if partidos_j:
                    for j in partidos_j:
                        anio = int(j.fecha_hora.strftime('%Y'))
                        mes = int(j.fecha_hora.strftime('%m'))
                        if anio == anio_actual and mes == mes_actual:
                            partidos_jugados.append(j)
                    cant_partidos_jugados = len(partidos_jugados)
                else:
                    cant_partidos_jugados = 0
                if partidos_t:
                    for t in partidos_t:
                        anio = int(t.fecha_hora.strftime('%Y'))
                        mes = int(t.fecha_hora.strftime('%m'))
                        if anio == anio_actual and mes == mes_actual:
                            partidos_totales.append(t)
                    cant_partidos_totales = len(partidos_totales)
                else:
                    cant_partidos_totales = 0
                if partidos_s:
                    for s in partidos_s:
                        anio = int(s.fecha_hora.strftime('%Y'))
                        mes = int(s.fecha_hora.strftime('%m'))
                        if anio == anio_actual and mes == mes_actual:
                            partidos_suspendidos.append(s)
                    cant_partidos_suspendidos = len(partidos_suspendidos)
                else:
                    cant_partidos_suspendidos = 0
                if partidos_nc:
                    for nc in partidos_nc:
                        anio = int(nc.fecha_hora.strftime('%Y'))
                        mes = int(nc.fecha_hora.strftime('%m'))
                        if anio == anio_actual and mes == mes_actual:
                            partidos_noconfirmados.append(nc)
                    cant_partidos_noconfirmados = len(partidos_noconfirmados)
                else:
                    cant_partidos_noconfirmados = 0
                resultado.append([c, cant_partidos_totales, cant_partidos_jugados, cant_partidos_suspendidos, cant_partidos_noconfirmados])
            resultado.sort(key = lambda resultado: resultado[2], reverse=True)
            return render(request, 'partidos/reporte_partidos_tipos.html', {'form': form, 'resultado': resultado})
    else:
        form = ReporteMesAnio()
    return render(request, 'partidos/reporte_partidos_tipos.html', {'form': form})
