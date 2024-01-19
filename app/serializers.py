from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *
Usermodel = get_user_model()
from rest_framework.response import Response

class UsersSerialiazers(serializers.ModelSerializer):
    passwordconfirm = serializers.CharField(write_only =True)
    class Meta:
        model = Usermodel
        fields = ['id','nome','email','password','passwordconfirm']
        extra_kwargs = {
            'password': {'write_only': True},
            }
        
    def validate(self, data):
        if data.get('password') != data.get('passwordconfirm'):
            raise serializers.ValidationError("As senhas não coincidem.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = Usermodel.objects.create_user(email = validated_data['email'], password = validated_data['password'],nome = validated_data['nome'])
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