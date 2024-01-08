from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from .views import UserLoginAPI, LogoutAPIView, ChangePasswordAPIView

app_name = 'account'

urlpatterns = [
    path('token/',TokenObtainPairView.as_view()),
    path('refrash/',TokenRefreshView.as_view()),
    path('verify/',TokenVerifyView.as_view()),
    path('login/', UserLoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('changepassword/', ChangePasswordAPIView.as_view(), name='change_password'),
]
