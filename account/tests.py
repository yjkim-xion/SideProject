from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from cars.models import CarSales, Car, UsedCarSales
from cars.views import PurchaseCarAPI
from unittest import mock
from datetime import datetime
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


# 유저로그인
class UserModelTest(TestCase):
    def test_login(self):
        client = APIClient()
        mock_date = datetime.now()
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


# 구매 테스트
class PurchaseCarAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test2', password='xion123!')
        self.car = Car.objects.create(
            brand='TestBrand',
            name='TestName',
            price=10000,
            version=1,
            is_sold=False
        )
        self.url = reverse('cars:purchases')  # 장고 템플릿 url처럼 작성해야함

    def test_purchase_car(self):
        self.client.force_authenticate(user=self.user)
        data = {'brand': self.car.brand, 'name': self.car.name}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Purchase successful')
        self.assertEqual(response.data['vin'], self.car.vin)
        self.assertEqual(response.data['price'], self.car.price)
        self.assertEqual(response.data['version'], self.car.version)

        self.car.refresh_from_db()
        self.assertTrue(self.car.is_sold)
        self.assertTrue(CarSales.objects.filter(car=self.car, user=self.user).exists())


# 반품 테스트
class RetrunCarAPITestcase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test2', password='xion123!')
        self.car = Car.objects.create(
            brand='TestBrand',
            name='TestName',
            price=10000,
            version=1,
            vin='wer123wer',
            is_sold=True
        )
        self.sales_record = CarSales.objects.filter(car=self.car).first()
        self.url = reverse('cars:returnCar')

    def test_return_car(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': self.car.name, 'version': self.car.version, 'vin': self.car.vin}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '반품 처리 되었습니다.')

        self.car.refresh_from_db()
        self.client.delete(self.sales_record)
        self.assertFalse(self.car.is_sold)


# 판매 테스트 (중고차행)
class SellUsedCarAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test2', password='xion123!')
        self.car = Car.objects.create(
            brand='TestBrand',
            name='TestName',
            price=10000,
            version=1,
            vin='wer123wer',
            is_sold=True
        )
        self.discount_rate = self.car.version * 10
        self.discounted_price = self.car.price * (1 - (self.discount_rate / 100))
        CarSales.objects.create(car=self.car, user=self.user)
        self.sales_record = CarSales.objects.filter(car=self.car).first()
        self.url = reverse('cars:sellcars')

    def test_sell_car(self):
        self.client.force_authenticate(user=self.user)

        data = {'name': self.car.name, 'brand': self.car.brand, 'version': self.car.version}
        response = self.client.post(self.url, data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['discounted_price'], self.discounted_price)

        self.car.refresh_from_db()
        self.assertFalse(self.car.is_sold)
        self.assertEqual(self.car.price, self.discounted_price)

        self.assertTrue(UsedCarSales.objects.filter(car=self.car, user=self.user).exists())
        self.assertFalse(CarSales.objects.filter(car=self.car).exists())
