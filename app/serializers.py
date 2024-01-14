from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *
Usermodel = get_user_model()

class UsersSerialiazers(serializers.ModelSerializer):
    class Meta:
        model = Usermodel
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            }
        
    def create(self, validated_data):
        user = Usermodel.objects.create_user(email = validated_data['email'], password = validated_data['password'],nome = validated_data['nome'],nasc = validated_data['nasc'])
        
        user.save()
        return user
    
class UsersLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    

class EnderecoSerialzers(serializers.ModelSerializer):
    class Meta:
        model = Enderecos
        fields = '__all__'


class DadosSerializers(serializers.Serializer):
    data_usuario = UsersSerialiazers()
    endereco_data = EnderecoSerialzers()