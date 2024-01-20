from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.test import RequestFactory
import requests

def Validation_password(password):
    senha = password
    tam = len(senha)
    
    if tam < 8:
        return Response({"message":"Senha muito curta"}, status = status.HTTP_400_BAD_REQUEST)
    
    for i,n in enumerate(str(senha)):
        if i == 0 and n.isnumeric():
            return Response({"message":"Não é possivel que a senha comece com números"}, status = status.HTTP_400_BAD_REQUEST) 
        if n.isalnum() == False:
            return Response({"message":"Caracteres especiais não são permitidos"}, status = status.HTTP_400_BAD_REQUEST)
    
    return Response(senha, status = status.HTTP_200_OK)

def Validation_cep(cep):
    if len(str(cep)) != 8:
        return Response({"message":"CEP invalido, por favor informe 8 digitos númericos"}, status = status.HTTP_400_BAD_REQUEST)
    else:
        url = (f'https://viacep.com.br/ws/{cep}/json/')
        
        response = requests.get(url)
        dados = response.json()
        if 'erro' in dados:
            return Response({"message":"O CEP informado não corresponde a nenhuma localidade "}, status = status.HTTP_400_BAD_REQUEST)    
        else:
            return Response(response.text, status = status.HTTP_200_OK)
    
    
def obter_token_jwt(email, password):
    factory = RequestFactory()
    request = factory.post('/token/', {'email': email, 'password': password})
    view = TokenObtainPairView.as_view()
    response = view(request)
    return response.data.get('access') 