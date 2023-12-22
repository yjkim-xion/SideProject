from django.utils.timezone import now
from rest_framework import generics, mixins, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from account.models import User
from .models import Car, CarSales, UsedCarSales, Version
from django.shortcuts import get_object_or_404
from .serializers import CarSerializer, CarSalesSerializer, UsedCarSalesSerializer, VersionSerializer


# 자동차 전체 목록
class CarsListAPI(generics.ListAPIView):
    permission_classes = []
    serializer_class = CarSerializer
    queryset = Car.objects.all().order_by('id')


# 자동차 디테일
class CarsDetailAPI(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = CarSerializer
    queryset = Car.objects.all()


# 구매
class PurchaseCarAPI(generics.GenericAPIView):
    serializer_class = CarSerializer, VersionSerializer

    def post(self, request, *args, **kwargs):
        brand = request.data.get('brand')
        name = request.data.get('name')

        car = Car.objects.filter(brand=brand, name=name).first()

        if not car:
            return Response({'error': '자동차 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if car.is_car_sold():
            return Response({'error': '이 자동차는 이미 판매 완료 되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        CarSales.objects.create(car=car, user=request.user, sale_date=now(), sale_price=car.price)
        car.is_sold = True
        car.save()
        return Response({'message': 'Purchase successful', 'vin': car.vin, 'price': car.price,})


# 반품
class ReturnCarAPI(generics.GenericAPIView):
    serializer_class = CarSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        vin = request.data.get('vin')
        car = get_object_or_404(Car, name=name, vin=vin)

        if not car.is_car_sold:
            return Response({'error': '이 차량은 판매할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        sales_record = CarSales.objects.filter(car=car).first()
        if sales_record:
            sales_record.delete()

        car.is_sold = False
        car.save()

        return Response({'message': '반품 처리 되었습니다.'}, status=status.HTTP_200_OK)


# 판매(중고차행)
class SellUsedCarAPI(generics.CreateAPIView):
    serializer_class = UsedCarSalesSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        brand = request.data.get('brand')
        vin = request.data.get('vin')
        versions = request.data.get('versions')

        car = get_object_or_404(Car, brand=brand, name=name, vin=vin)
        print(car)
        versions = get_object_or_404(Version,versions=versions)
        print(versions)
        discount_rate = versions * 10

        if not CarSales.objects.filter(car=car, user=request.user).exists():
            return Response({'error': '소유한 차만 판매가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if not car.is_car_sold:
            return Response({'error': '이 차량은 판매할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if UsedCarSales.objects.filter(car=car, user=request.user).exists():
            return Response({'error': '이 자동차는 이미 판매 완료 되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        sale_price = car.price
        discounted_price = sale_price * (1 - (discount_rate / 100))

        UsedCarSales.objects.create(
            car=car,
            user=request.user,
            sale_date=now(),
            sale_price=discounted_price,
            discount_rate=discount_rate
        )
        sales_record = CarSales.objects.filter(car=car).first()

        if sales_record:
            sales_record.delete()

        car.is_sold = False
        car.save()

        car.price = discounted_price
        car.save()

        return Response({'message': 'Car sold', 'discounted_price': discounted_price}, status=status.HTTP_201_CREATED)


# 버전별 모든 자동차
class VersionAPI(generics.ListAPIView):
    permission_classes = []
    serializer_class = CarSerializer

    def get_queryset(self):
        versions = self.kwargs.get('versions')
        return Version.objects.filter(versions=versions)


# 자동차별 버전
class CarVersionsAPI(generics.ListAPIView):
    permission_classes = []
    serializer_class = VersionSerializer

    def get_queryset(self):
        car_id = self.kwargs.get('car_id')
        return Version.objects.filter(car_id=car_id)
