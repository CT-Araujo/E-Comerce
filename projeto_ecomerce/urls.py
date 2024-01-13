from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/',TokenObtainPairView.as_view(), name = 'token'),
    path('login/',views.UserLogin.as_view(), name = 'login'),
    path('',views.UsersViews.as_view(),name='usuarios'),
]
