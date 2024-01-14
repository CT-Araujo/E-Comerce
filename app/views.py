from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from .serializers import *
from .validators import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
Usermodel = get_user_model()


class UsersViews(APIView):
    def get(self, request):
        filtro = request.query_params.get('email', None)
        if filtro:
            user = Users.objects.get(email=filtro)
            enderecos = Enderecos.objects.filter(user=user.id)

            user_data = {
                "id": user.id,
                "data_create": user.data_create,
                "nome": user.nome,
                "email": user.email,
                "nasc": user.nasc,
            }

            endereco_data = [{
                "cidade": endereco.cidade,
                "bairro": endereco.bairro,
                "cep": endereco.cep,
                "rua": endereco.rua,
                "numero": endereco.numero
            } for endereco in enderecos] # Quando usar o for, instancie o valor unico(endereco) ao invés do grupo(enderecos)

            dados = {
                "Usuario": user_data,
                "Endereco": endereco_data
            }

            return Response(dados, status=status.HTTP_200_OK)
        dados = Usermodel.objects.all()
        serialized = UsersSerialiazers(dados, many = True)
        return Response(serialized.data, status = status.HTTP_200_OK)
    
    
    def post(self, request):
        serializers = UsersSerialiazers(data = request.data)
        if serializers.is_valid(raise_exception=True):
            
            email = serializers.validated_data.get('email')
            password = serializers.validated_data.get('password')
            id = serializers.validated_data.get('id')
            
            confirma_senha = Validation_password(password)
            
            if confirma_senha.status_code == 200:
                user = serializers.create(serializers.validated_data)
                if user:
                    token = obter_token_jwt(email, password)
                    if token:
                        login = {
                            "token": token,
                            "id": id,
                            "email": email 
                        }
                        return Response(login, status = status.HTTP_201_CREATED)
                return Response(status = status.HTTP_401_UNAUTHORIZED)  
            return(confirma_senha)  
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk = None):
        if request.method == 'PATCH':
            filtro = request.query_params.get('email', None)
            existe = Users.objects.filter(email = filtro).exists()
            
            token = request.headers.get('Authorization')
            
            if existe:
                user = Users.objects.get(email = filtro)
                if token:
                    serializer = UsersSerialiazers(user, data= request.data, partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status= status.HTTP_200_OK)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class UserLoginViews(APIView):
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
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class EnderecoViews(APIView):
    def get(self,request):
        dados = Enderecos.objects.all()
        serializers = EnderecoSerialzers(dados, many = True)
        return Response(serializers.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializers = EnderecoSerialzers(data = request.data)
        if serializers.is_valid():
            
            if Validation_cep(serializers.validated_data['cep']):
                new_endereco = Enderecos.objects.create(
                    id_user =  serializers.validated_data['id_user'],
                    cidade = serializers.validated_data['cidade'],
                    bairro = serializers.validated_data['bairro'],
                    cep = serializers.validated_data['cep'],
                    rua = serializers.validated_data['rua'],
                    numero = serializers.validated_data['numero'],
                )       
                if Enderecos.objects.filter(id_user = serializers.validated_data["id_user"]).count() < 2:
                    new_endereco.save()
                    return Response(status = status.HTTP_200_OK)
                return Response({"message":"Já existem dois endereços cadastrados nesse mesmo usuário"}, status = status.HTTP_400_BAD_REQUEST)
            return Response({"message":"Erro na validação"},status = status.HTTP_400_BAD_REQUEST)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        get_id = request.query_params.get('id',None)
        try:
            dado = Enderecos.objects.filter(user= get_id).first()
            dado.delete()
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]  
        elif self.request.method == 'PATCH':  
            return [IsAuthenticated()] 
        return super().get_permissions()
    
        
            
        