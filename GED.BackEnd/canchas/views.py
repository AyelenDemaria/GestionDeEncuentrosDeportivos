from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework import permissions
from .models import Cancha
from vouchers.models import Voucher
from .serializers import CanchaSerializer, CanchaGetSerializer
from django.utils import timezone
from datetime import datetime

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
        print (canchas)
        serializer = CanchaGetSerializer(canchas, many=True)
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
        serializer = CanchaGetSerializer(canchas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def reporte_ingresos(request):
    canchas = Cancha.objects.all()
    total_abono = 0
    for c in canchas:
        total_abono += c.abono_mensual
    fecha_hora_actual = timezone.localtime(timezone.now())
    fecha_actual = fecha_hora_actual.date()
    #mes_actual = fecha_actual.month()
    mes_actual = datetime.today().month
    vouchers_all = Voucher.objects.all()
    vouchers = []
    if vouchers_all:
        total_voucher = 0
        for v in vouchers_all:
            mes_voucher = int(v.fecha_emision.strftime('%m'))
            #mes_voucher = v.fecha_emision.month
            if mes_actual == mes_voucher:
                vouchers.append(v)
        if vouchers:
            for j in vouchers:
                subtotal = v.cancha.valor_uso + v.cancha.valor_referi
                total_voucher += subtotal
        else:
            total_voucher = 0
    else:
        total_voucher = 0
    resultado =  []
    for i in canchas:
        vouchers_cancha = Voucher.objects.filter(cancha_id=i.id)
        if vouchers_cancha:
            for j in vouchers_cancha:
                total_vouchers = []
                mes_voucher = int(j.fecha_emision.strftime('%m'))
                if mes_actual == mes_voucher:
                    total_vouchers.append(j)
            if total_vouchers:
                cant_vouchers =  len(total_vouchers)
                total_vouchers_cancha = cant_vouchers * (i.valor_uso + i.valor_referi)
            else:
                cant_vouchers = 0
                total_vouchers_cancha = 0
        else:
            cant_vouchers = 0
            total_vouchers_cancha = 0
        resultado.append([i,i.abono_mensual,cant_vouchers,total_vouchers_cancha])
    return render(request, 'canchas/reporte_ingresos.html', {'resultado': resultado, 'total_abono': total_abono, 'total_voucher': total_voucher, "mes_actual":mes_actual})
