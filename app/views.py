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
    
    def delete(self, request):
        filtro = request.query_params.get('id', None)
        user = Users.objects.get(id = filtro)
        if user:
            user.delete()
            return Response(status = status.HTTP_200_OK)
        
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class UserLoginViews(APIView):
        def post(self,request):
            email = request.data.get('email')
            password = request.data.get('password')
            existe = Users.objects.filter(email = email).exists()
            
            if email is None or password is None:
                return Response({"message":"Por favor preencha corretamente todos os campos"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                if existe:
                    user = Users.objects.get(email = email)
                    login = authenticate(email = email, password = password)
                    if login:
                        token = obter_token_jwt(email, password)
                        if token:
                            dados = {
                                "token": token,
                                "email": email,
                                "id": user.id
                            }
                            return Response(dados, status = status.HTTP_200_OK)
                        return Response({"message":"Erro na geração do token"}, status = status.HTTP_400_BAD_REQUEST)
                    return Response({"message":"Erro na autenticação do usuário"}, status = status.HTTP_401_UNAUTHORIZED)
                return Response({"message":"Usuário não encontrado no banco de dados"}, status = status.HTTP_404_NOT_FOUND)                 
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class EnderecoViews(APIView):
    def get(self,request):
        dados = Enderecos.objects.all()
        serializers = EnderecoSerialzers(dados, many = True)
        return Response(serializers.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializers = EnderecoSerialzers(data = request.data)
        if serializers.is_valid():
            cep = serializers.validated_data['cep']
            
            validated = Validation_cep(cep)
            
            if validated.status_code == 200:
                dados = eval(validated.data)
                
                if Enderecos.objects.filter(user = serializers._validated_data['user']).count() < 2:
                    
                    new_endereco = Enderecos.objects.create(
                        user =  serializers.validated_data['user'],
                        cidade = dados['localidade'],
                        bairro = dados['bairro'],
                        cep = cep,
                        rua = dados['logradouro'],                    
                    )
                    
                    new_endereco.save()
                    endreco_serialized = EnderecoSerialzers(new_endereco)
                    return Response(endreco_serialized.data, status = status.HTTP_201_CREATED)
                
                return Response({"message":"Já existem dois endereços cadastrados neste usuário"}, status = status.HTTP_400_BAD_REQUEST)
            return Response({"message": validated.data}, status = status.HTTP_400_BAD_REQUEST)
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
    
        

class ProdutosViews(APIView):
    def get(self,request):
        filtro_name = request.query_params.get('nome', None)
        filtro_categoria = request.query_params.get('categoria', None)
        
        if filtro_name:
            dados = Produtos.objects.filter(nome = filtro_name)
            serializers = ProdutosSerializers(dados, many = True )
            return Response( serializers.data, status = status.HTTP_200_OK)
        
        if filtro_categoria:
            dados = Produtos.objects.filter(categoria = filtro_categoria)
            serializers = ProdutosSerializers(dados, many = True )
            return Response( serializers.data, status = status.HTTP_200_OK)
        
        if filtro_categoria and filtro_name:
            dados = Produtos.objects.filter(nome = filtro_name, categoria = filtro_categoria )
            serializers = ProdutosSerializers(dados, many = True )
            return Response( serializers.data, status = status.HTTP_200_OK)
        
        dados = Produtos.objects.all()
        serializers = ProdutosSerializers(dados, many = True )
        return Response( serializers.data, status = status.HTTP_200_OK)
    
    
    def post(self, request):
        serializers = ProdutosSerializers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        if request.method == 'PATCH':
            filtro = request.query_params.get('id', None)
            existe = Produtos.objects.filter(id = filtro).exists()
        
            if existe:
                produto = Produtos.objects.get(id = filtro)
                serializer = ProdutosSerializers(produto, data= request.data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status= status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [IsAuthenticated()]
    
    