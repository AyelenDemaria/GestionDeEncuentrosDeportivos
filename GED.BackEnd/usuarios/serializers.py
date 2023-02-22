from rest_framework import serializers
from .models import Perfil
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'is_staff']

class PerfilSerializer(serializers.ModelSerializer):
    #user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Perfil
        fields = ["user_id","documento","fecha_nacimiento","telefono","sexo","puntos_acum" ]


class UserLoginSerializer(serializers.Serializer):

    # Campos que vamos a requerir
    username = serializers.CharField()
    password = serializers.CharField()

    # Primero validamos los datos
    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        #self.context['user'] = user
        return data

    def create(self,validated_data):
        return User.objects.create(**validated_data)
        #return self.context['user']
