from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from .serializers import *
from .validators import *
Usermodel = get_user_model()


class UsersViews(APIView):
    def get(self, request):
        dados = Usermodel.objects.all()
        serialized = UsersSerialiazers(dados, many = True)
        return Response(serialized.data, status = status.HTTP_200_OK)
    
    
    def post(self, request):
        serializers = UsersSerialiazers(data = request.data)
        if serializers.is_valid(raise_exception=True):
            
            email = serializers.validated_data.get('email')
            password = serializers.validated_data.get('password')
            nome = serializers.validated_data.get('nome')
            
            confirma_senha = Validation_password(password)
            
            if confirma_senha.status_code == 200:
                user = serializers.create(serializers.validated_data)
                if user:
                    token = obter_token_jwt(email, password)
                    if token:
                        login = {
                            "token": token,
                            "email": email 
                        }
                        return Response(login, status = status.HTTP_201_CREATED)
                return Response(status = status.HTTP_401_UNAUTHORIZED)  
            return(confirma_senha)  
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class UserLogin(APIView):
    def post(self,request):
        serializers = UsersLoginSerializer(data = request.data)
        if serializers.is_valid():
            email = serializers.validated_data.get('email')
            password = serializers.validated_data.get('password')
            existe = Usermodel.objects.filter(email = email).exists()
            
        if existe:
            user = authenticate(username = email, password = password)
            if user:
                token = obter_token_jwt(email, password)
                if token:
                    login = {
                        "token": token,
                        "email": email
                    }  
                    return Response(login, status = status.HTTP_200_OK)              
            return Response({"message":"Erro na autenticação"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response({"message":"O usuário informado não existe"}, status = status.HTTP_404_NOT_FOUND)
        