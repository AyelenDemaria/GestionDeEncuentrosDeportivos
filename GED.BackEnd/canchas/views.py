from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework import permissions
from .models import Cancha
from .serializers import CanchaSerializer, CanchaGetSerializer

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
        pk = int(request.data['deporte_id'])
        canchas = Cancha.objects.filter(deporte_id=pk)
        serializer = CanchaGetSerializer(canchas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
