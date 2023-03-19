from rest_framework import serializers
from .models import Perfil
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'username', 'password', 'first_name', 'last_name', 'is_staff']

class PerfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    #print("USER", user)
    class Meta:
        model = Perfil
        fields = ["user","documento","fecha_nacimiento","telefono","sexo","puntos_acum" ]

    def create(self, validated_data):
        #print("---------------")
        #print(validated_data)
        #print("---------------")
        user_data = validated_data.pop('user')
        user_instance = User.objects.create(
            username=user_data['username'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=user_data['is_staff']
            )
        user_instance.save()

        perfil_instance = Perfil.objects.create(
            **validated_data, user=user_instance)
        perfil_instance.save()
        return perfil_instance


class UserLoginSerializer(serializers.Serializer):

    # Campos que vamos a requerir
    username = serializers.CharField()
    password = serializers.CharField()
    #print("username and password:", username, password)
    # Primero validamos los datos
    def validate(self, data):
        print("validate", data)
        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        try:
            user = User.objects.get(username=data['username'])
        except:
            user = None
        print("user", user)
        if user:
            if user.password == data['password']:
                authenticate(user)
            else:
                print('acaaaa')
                authenticate(username=data['username'], password=data['password'])
            # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
            self.context['user'] = user
            return data
        raise serializers.ValidationError('Las credenciales no son válidas')

    def create(self,validated_data):
        print("create")
        #return User.objects.create(**validated_data)
        return self.context['user']
