from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework import permissions
from .models import Cancha, CanchaPrecio
from vouchers.models import Voucher
from .serializers import CanchaSerializer, CanchaGetSerializer, CanchaPrecioSerializer
from django.utils import timezone
from datetime import datetime
from .forms import ReporteMesAnio

meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

class CanchaListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        Lista de todas las canchas
        '''
        #canchas = Cancha.objects.all().values()
        canchas = Cancha.objects.all()
        if canchas:
            canchas_rta = []
            fecha_hora_actual = timezone.localtime(timezone.now())
            fecha_actual = fecha_hora_actual.date()
            for c in canchas:
                cancha_precio = CanchaPrecio.objects.filter(cancha = c, fecha__lte=fecha_actual).latest('fecha')
                canchas_rta.append(cancha_precio)
        serializer = CanchaPrecioSerializer(canchas_rta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return JsonResponse(list(canchas), safe=False, status=status.HTTP_200_OK)

class CanchaByDeporteListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        Lista de todas las canchas de un deporte
        '''
        print(request.GET.get('deporte_id'))
        #print("body:",request.body)
        pk = int(request.GET.get('deporte_id'))
        canchas = Cancha.objects.filter(deporte_id=pk)
        if canchas:
            canchas_rta = []
            fecha_hora_actual = timezone.localtime(timezone.now())
            fecha_actual = fecha_hora_actual.date()
            for c in canchas:
                cancha_precio = CanchaPrecio.objects.filter(cancha = c, fecha__lte=fecha_actual).latest('fecha')
                canchas_rta.append(cancha_precio)
            serializer = CanchaPrecioSerializer(canchas_rta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def reporte_ingresos(request):
    if request.method == "POST":
        form = ReporteMesAnio(request.POST)
        if form.is_valid():
            mes_actual = int(form.cleaned_data["mes"])
            anio_actual = int(form.cleaned_data["anio"])
        canchas = Cancha.objects.all()
        total_abono = 0
        for c in canchas:
            ultimo_abono = CanchaPrecio.objects.filter(cancha=c, fecha__year__lte=anio_actual, fecha__month__lte=mes_actual).latest('fecha')
            total_abono += ultimo_abono.abono_mensual
            #total_abono += c.abono_mensual
        vouchers_all = Voucher.objects.all()
        vouchers_emitidos = []
        vouchers_canjeados = []
        if vouchers_all:
            total_vouchers_emitidos = 0
            total_vouchers_canjeados = 0
            for v in vouchers_all:
                mes_voucher = int(v.fecha_emision.strftime('%m'))
                #mes_voucher = v.fecha_emision.month
                if mes_actual == mes_voucher:
                    vouchers_emitidos.append(v)
                if v.fecha_canje is not None:
                    mes_canjeo = int(v.fecha_canje.strftime('%m'))
                    if mes_actual == mes_canjeo:
                        vouchers_canjeados.append(v)
            if vouchers_emitidos:
                for j in vouchers_emitidos:
                    subtotal = j.cancha.valor_uso + j.cancha.valor_referi
                    total_vouchers_emitidos += subtotal
            else:
                total_vouchers_emitidos = 0
            if vouchers_canjeados:
                for v in vouchers_canjeados:
                    subtotal = v.cancha.valor_uso + v.cancha.valor_referi
                    total_vouchers_canjeados += subtotal
            else:
                total_vouchers_canjeados = 0
        else:
            total_voucher_emitidos = 0
            total_vouchers_canjeados = 0
        resultado =  []
        for i in canchas:
            ultimo_abono_i = CanchaPrecio.objects.filter(cancha=i, fecha__year__lte=anio_actual, fecha__month__lte=mes_actual).latest('fecha')
            print("-----------------ultimo abono:",ultimo_abono_i,i.nombre)
            abono_mensual_i = ultimo_abono_i.abono_mensual
            vouchers_cancha = Voucher.objects.filter(cancha__cancha=i)
            if vouchers_cancha:
                total_vouchers_cancha = 0
                total_vouchers_canj = 0
                vouchers_emitidos = []
                vouchers_canjeados = []
                for j in vouchers_cancha:
                    mes_voucher = int(j.fecha_emision.strftime('%m'))
                    if mes_actual == mes_voucher:
                        vouchers_emitidos.append(j)
                    if j.fecha_canje is not None:
                        mes_canjeo = int(j.fecha_canje.strftime('%m'))
                        if mes_actual == mes_canjeo:
                            vouchers_canjeados.append(j)
                if vouchers_emitidos:
                    for v in vouchers_emitidos:
                        subtotal = v.cancha.valor_uso + v.cancha.valor_referi
                        total_vouchers_cancha += subtotal
                    cant_vouchers =  len(vouchers_emitidos)
                else:
                    cant_vouchers = 0
                    total_vouchers_cancha = 0
                if vouchers_canjeados:
                    for v in vouchers_canjeados:
                        subtotal = v.cancha.valor_uso + v.cancha.valor_referi
                        total_vouchers_canj += subtotal
                    cant_vouchers_canjeados =  len(vouchers_canjeados)
                else:
                    cant_vouchers_canjeados = 0
                    total_vouchers_canj = 0
            else:
                cant_vouchers = 0
                total_vouchers_cancha = 0
                cant_vouchers_canjeados = 0
                total_vouchers_canj = 0
            ganancia = total_abono - total_vouchers_canjeados
            resultado.append([i,abono_mensual_i,cant_vouchers,total_vouchers_cancha,cant_vouchers_canjeados,total_vouchers_canj])
        return render(request, 'canchas/reporte_ingresos.html', {'form': form, 'resultado': resultado, 'total_abono': total_abono, 'total_vouchers_emitidos': total_vouchers_emitidos,"total_vouchers_canjeados": total_vouchers_canjeados, 'ganancia' : ganancia})
    else:
        form = ReporteMesAnio()
    return render(request, 'canchas/reporte_ingresos.html', {'form': form})
