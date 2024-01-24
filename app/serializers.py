from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *
Usermodel = get_user_model()
from rest_framework.response import Response
from google.auth.transport import requests
from google.oauth2 import id_token
from projeto_ecomerce.settings import *

class UsersSerialiazers(serializers.ModelSerializer):
    passwordconfirm = serializers.CharField(write_only =True)
    class Meta:
        model = Usermodel
        fields = ['id','nome','email','password','passwordconfirm','user_google',]
        extra_kwargs = {
            'password': {'write_only': True},
            }
        
    def validate(self, data):
        if data.get('password') != data.get('passwordconfirm'):
            raise serializers.ValidationError("As senhas não coincidem.")
        return data
    
    def create(self, validated_data):
        if validated_data['user_google'] == False:
            validated_data.pop('confirm_password', None)
            user = Usermodel.objects.create_user(email = validated_data['email'], password = validated_data['password'],nome = validated_data['nome'], user_google = validated_data['user_google'])
            user.save()
            return user
        
    
class UsersLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    

class EnderecoSerialzers(serializers.ModelSerializer):
    class Meta:
        model = Enderecos
        fields = '__all__'

class ProdutosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'
        
        
class UserGoogleSerializers(serializers.Serializer):
    token_google = serializers.CharField(write_only = True)
    user_google = serializers.CharField(write_only = True)
    def create(self, validated_data):
        id_info = id_token.verify_oauth2_token(validated_data['token_google'], requests.Request(), GOOGLE_OAUTH2_CLIENT_ID)
        user = Usermodel.objects.create_user(email = id_info.get('email'), nome = id_info.get('name'), password = id_info['sub'], google_id = id_info['sub'], user_google = validated_data['user_google'])
        
        user.save()
        return user