from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/',TokenObtainPairView.as_view(), name = 'token'),
    path('login/',views.UserLoginViews.as_view(), name = 'login'),
    path('endereco/',views.EnderecoViews.as_view(), name = 'endereco'),
    path('produtos/',views.ProdutosViews.as_view(), name = 'produtos'),
    path('',views.UsersViews.as_view(),name='usuarios'),
    path('google/',views.GoogleUserViews.as_view(),name='usuarios_google'),
]
