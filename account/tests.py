from django.test import TestCase
# from django.contrib.auth.models import User
from unittest import mock
from datetime import datetime
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


# 유저로그인
class UserModelTest(TestCase):
    def test_default_values(self):
        client = APIClient()
        mock_date = datetime(2023,12,19,15,53,45)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = mock_date
            user = User.objects.create(username='test2', password='xion123!')

            refresh = RefreshToken.for_user(user=user)
            access = refresh.access_token
            client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {access}"
            )
            self.assertEquals(user.username, 'test2')
            self.assertEquals(user.password, 'xion123!')
            self.assertEquals(user.is_active, True)
            self.assertEquals(user.is_staff, False)
            self.assertEquals(user.is_superuser, False)
            self.assertEquals(user.created_at, mock_date)
            self.assertEquals(user.updated_at, mock_date)
            self.assertEquals(user.last_login, mock_date)



