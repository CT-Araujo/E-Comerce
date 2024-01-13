from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework.response import Response
from rest_framework import status
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email,nome,nasc, password = None):
        if not email:
            return Response({"message":"O email não foi informado"}, status = status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({"message":"A senha não foi informado"}, status = status.HTTP_400_BAD_REQUEST)
        
        if not nome:
            return Response({"message":"O nome do Usuário não foi informado"}, status = status.HTTP_400_BAD_REQUEST)
        
        if not nasc:
            return Response({"message":"O nome do Usuário não foi informado"}, status = status.HTTP_400_BAD_REQUEST)
            
        email = self.normalize_email(email)
        user = self.model(email = email, nome = nome, nasc = nasc)
        user.set_password(password)
        user.save()
        
        return user

class Users(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, auto_created = True, unique = True,editable = False)
    nome = models.CharField(max_length = 100, blank = False)
    email = models.EmailField(max_length = 120, unique = True, blank = False)
    nasc = models.DateField(blank = False, null = False)
    historico = models.JSONField(blank = True, null = True)
    endereço = models.JSONField(max_length = 200, blank = True, null = True)
    data_create = models.DateField(auto_now_add = True, auto_created = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome','nasc']
    objects = UserManager()

