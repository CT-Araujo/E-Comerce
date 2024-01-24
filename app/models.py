from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework.response import Response
from rest_framework import status
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email,nome, user_google,google_id, password = None):
        if not email:
            return Response({"message":"O email não foi informado"}, status = status.HTTP_400_BAD_REQUEST)
        if user_google == False:
            if not password:
                return Response({"message":"A senha não foi informada"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            if not google_id:
                return Response({"message":"O ID  não foi informado"}, status = status.HTTP_400_BAD_REQUEST)
            password = google_id
        
        if not nome:
            return Response({"message":"O nome do Usuário não foi informado"}, status = status.HTTP_400_BAD_REQUEST)

            
        email = self.normalize_email(email)
        user = self.model(email = email, nome = nome, google_id = google_id, user_google = user_google)
        user.set_password(password)
        user.save()
        
        return user

class Users(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, auto_created = True, unique = True,editable = False)
    nome = models.CharField(max_length = 100, blank = False)
    email = models.EmailField(max_length = 120, unique = True, blank = False)
    historico = models.JSONField(blank = True, null = True)
    data_create = models.DateField(auto_now_add = True, auto_created = True)
    nasc = models.DateField(blank = True, null = True)
    user_google = models.BooleanField(blank = False, null = False, editable = False, default = False)
    google_id = models.CharField(blank = True, null = True, editable = False, unique = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome','user_google']
    objects = UserManager()
    


class Enderecos(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    cidade = models.CharField(max_length = 50, blank = False, null = True)
    bairro = models.CharField(max_length = 50, blank = False, null = True)
    cep = models.IntegerField(blank = False, null = False)
    rua = models.CharField(max_length = 100, blank = False, null = True)
    numero = models.IntegerField(blank = False, null = True)
    

class Produtos(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, auto_created = True, unique = True,editable = False)
    nome = models.CharField(max_length = 50, blank = False, null = False)
    descricao = models.CharField(max_length = 50, blank = True, null = True)
    categoria = models.CharField(max_length = 50, blank = False, null = False)
    loja = models.CharField(max_length = 50, blank = False, null = False)
    preco = models.FloatField(max_length = 5, blank = False, null = False)
    imposto = models.FloatField(max_length = 5, blank = False, null = False)
    localizacao = models.CharField(max_length = 50, blank = False, null = False)
    
    
       
