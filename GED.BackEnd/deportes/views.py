from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Deporte
from .serializers import DeporteSerializer

class DeporteListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        Lista de todos los deportes
        '''
        deportes = Deporte.objects.all()
        serializer = DeporteSerializer(deportes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
