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
from .forms import ReporteMesAnio, ReporteAnio

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
        #canchas = Cancha.objects.all()
        fecha_hora_actual = timezone.localtime(timezone.now())
        fecha_actual = fecha_hora_actual.date()
        canchas = Cancha.object.filter(fecha_ingreso__lte=fecha_actual,fecha_baja__isnull=True)
        if canchas:
            canchas_rta = []
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
        fecha_hora_actual = timezone.localtime(timezone.now())
        fecha_actual = fecha_hora_actual.date()
        canchas = Cancha.objects.filter(deporte_id=pk,fecha_ingreso__lte=fecha_actual,fecha_baja__isnull=True)
        if canchas:
            canchas_rta = []
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
            try:
                ultimo_abono = CanchaPrecio.objects.filter(cancha=c, fecha__year__lte=anio_actual, fecha__month__lte=mes_actual).latest('fecha')
            except CanchaPrecio.DoesNotExist:
                ultimo_abono = None
            if ultimo_abono is not None:
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
                anio_voucher = int(v.fecha_emision.strftime('%Y'))
                #mes_voucher = v.fecha_emision.month
                if mes_actual == mes_voucher and anio_voucher == anio_actual:
                    vouchers_emitidos.append(v)
                if v.fecha_canje is not None:
                    mes_canjeo = int(v.fecha_canje.strftime('%m'))
                    anio_canjeo = int(v.fecha_canje.strftime('%Y'))
                    if mes_actual == mes_canjeo and anio_canjeo == anio_actual:
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
        for i in canchas_vigentes:
            abono_mensual_i = 0
            try:
                ultimo_abono_i = CanchaPrecio.objects.filter(cancha=i, fecha__year__lte=anio_actual, fecha__month__lte=mes_actual).latest('fecha')
            except CanchaPrecio.DoesNotExist:
                ultimo_abono_i = None
            if ultimo_abono_i is not None:
                abono_mensual_i = ultimo_abono_i.abono_mensual
            vouchers_cancha = Voucher.objects.filter(cancha__cancha=i)
            if vouchers_cancha:
                total_vouchers_cancha = 0
                total_vouchers_canj = 0
                vouchers_emitidos = []
                vouchers_canjeados = []
                for j in vouchers_cancha:
                    mes_voucher = int(j.fecha_emision.strftime('%m'))
                    anio_voucher = int(j.fecha_emision.strftime('%Y'))
                    if mes_actual == mes_voucher  and anio_voucher == anio_actual:
                        vouchers_emitidos.append(j)
                    if j.fecha_canje is not None:
                        mes_canjeo = int(j.fecha_canje.strftime('%m'))
                        anio_canjeo = int(j.fecha_canje.strftime('%Y'))
                        if mes_actual == mes_canjeo and anio_canjeo == anio_actual:
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
            resultado.append([i,abono_mensual_i,cant_vouchers,total_vouchers_cancha,cant_vouchers_canjeados,total_vouchers_canj])
        ganancia = total_abono - total_vouchers_canjeados
        ganancia_posible = total_abono - total_vouchers_emitidos
        return render(request, 'canchas/reporte_ingresos.html', {'form': form, 'resultado': resultado, 'total_abono': total_abono, 'total_vouchers_emitidos': total_vouchers_emitidos,"total_vouchers_canjeados": total_vouchers_canjeados, 'ganancia' : ganancia,'ganancia_posible': ganancia_posible})
    else:
        form = ReporteMesAnio()
    return render(request, 'canchas/reporte_ingresos.html', {'form': form})


def reporte_ganancias(request):
    if request.method == "POST":
        form = ReporteAnio(request.POST)
        if form.is_valid():
            #mes_actual = int(form.cleaned_data["mes"])
            anio_actual = int(form.cleaned_data["anio"])
        canchas = Cancha.objects.all()
        vouchers_all = Voucher.objects.all()
        ganancia_total = 0
        resultado = []
        fecha_hora_actual = timezone.localtime(timezone.now())
        fecha_actual = fecha_hora_actual.date()
        mes_actual = fecha_actual.strftime('%m')
        anio_actual_2 = fecha_actual.strftime('%Y')
        if int(anio_actual_2) == anio_actual:
            fin = int(mes_actual) + 1
        else:
            fin = 13
        for i in range(1,fin):
            total_abono = 0
            canchas_vigentes = []
            for cancha in canchas:
                mes_ingreso = int(cancha.fecha_ingreso.strftime('%m'))
                anio_ingreso = int(cancha.fecha_ingreso.strftime('%Y'))
                if mes_ingreso <= i and anio_ingreso <= anio_actual:
                    if cancha.fecha_baja is not None:
                        mes_baja = int(cancha.fecha_baja.strftime('%m'))
                        anio_baja = int(cancha.fecha_baja.strftime('%Y'))
                        if i < mes_baja and anio_actual <= anio_baja:
                            canchas_vigentes.append(cancha)
                    else:
                        canchas_vigentes.append(cancha)
            for c in canchas_vigentes:
                try:
                    ultimo_abono = CanchaPrecio.objects.filter(cancha=c, fecha__year__lte=anio_actual, fecha__month__lte=i).latest('fecha')
                except CanchaPrecio.DoesNotExist:
                    ultimo_abono = None
                if ultimo_abono is not None:
                    total_abono += ultimo_abono.abono_mensual
                #total_abono += c.abono_mensual
            vouchers_canjeados = []
            if vouchers_all:
                total_vouchers_canjeados = 0
                for v in vouchers_all:
                    if v.fecha_canje is not None:
                        mes_canjeo = int(v.fecha_canje.strftime('%m'))
                        anio_canjeo = int(v.fecha_canje.strftime('%Y'))
                        if i == mes_canjeo and anio_canjeo == anio_actual:
                            vouchers_canjeados.append(v)
                if vouchers_canjeados:
                    for k in vouchers_canjeados:
                        subtotal = k.cancha.valor_uso + k.cancha.valor_referi
                        total_vouchers_canjeados += subtotal
                else:
                    total_vouchers_canjeados = 0
            else:
                total_vouchers_canjeados = 0
            ganancia_mes = total_abono - total_vouchers_canjeados
            ganancia_total += ganancia_mes
            resultado.append([meses[i-1], total_abono, total_vouchers_canjeados, ganancia_mes])
        return render(request, 'canchas/reporte_ganancias.html', {'form': form, 'resultado': resultado, 'ganancia_total': ganancia_total})
    else:
        form = ReporteAnio()
    return render(request, 'canchas/reporte_ganancias.html', {'form': form})
