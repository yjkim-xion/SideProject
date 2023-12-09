from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    idx = models.BigAutoField(primary_key=True)

    username = models.CharField(help_text='유저 명', max_length=255, unique=True)
    password = models.CharField(help_text='유저 패스워드', max_length=128)

    is_staff = models.BooleanField(help_text='staff 권한 여부', default=False)
    is_superuser = models.BooleanField(help_text='root 권한 여부', default=False)
    is_active = models.BooleanField(help_text='계정 활성화 여부', default=True)

    created_at = models.DateTimeField(help_text='생성일', verbose_name='date joined', auto_now_add=True)
    updated_at = models.DateTimeField(help_text='변경일', auto_now=True)
    last_login = models.DateTimeField(help_text='마지막 로그인', blank=True, null=True)
