from cars.logger import user_logger
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Car, CarSales, UsedCarSales, Version
from .serializers import CarSerializer, UsedCarSalesSerializer, VersionSerializer,CustomVersionSerializer

logger = user_logger()

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
            logger.info(f'[[{request.user}]-{name}- 자동차 정보 오류]')
            return Response({'error': '자동차 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if car.is_car_sold():
            logger.info(f'[[{request.user}]-{car}- 자동차 정보 오류]')
            return Response({'error': '이 자동차는 이미 판매 완료 되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        CarSales.objects.create(car=car, user=request.user, sale_date=now(), sale_price=car.price)
        car.is_sold = True
        car.save()
        print(car, request.user)
        logger.info(f'[{request.user}-{car}]-Purchase successful')
        return Response({'message': 'Purchase successful', 'vin': car.vin, 'price': car.price})


# 반품
class ReturnCarAPI(generics.GenericAPIView):
    serializer_class = CarSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        vin = request.data.get('vin')
        car = get_object_or_404(Car, name=name, vin=vin)

        if not car.is_sold:
            logger.info(f'[{car}]- 팔리지 않은 차량이라 반품 불가')
            return Response({'error': '이 차량은 판매할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        sales_record = CarSales.objects.filter(car=car).first()
        if sales_record:
            sales_record.delete()

        car.is_sold = False
        car.save()
        logger.info(f'[{car}]- 반품처리 완료')
        return Response({'message': '반품 처리 되었습니다.'}, status=status.HTTP_200_OK)


# 판매(중고차행)
class SellUsedCarAPI(generics.CreateAPIView):
    serializer_class = UsedCarSalesSerializer

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        brand = request.data.get('brand')
        vin = request.data.get('vin')

        car = get_object_or_404(Car, brand=brand, name=name, vin=vin)
        print(car)

        version = Version.objects.filter(car=car).first()
        print(version)

        if not version:
            logger.info(f'[{name}] - 해당 차량의 버전 정보 오류')
            return Response({'error': '해당 차량의 버전 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        discount_rate = version.versions * 10

        if not CarSales.objects.filter(car=car, user=request.user).exists():
            logger.info(f'[{request.user}] - {car} - 소유자 불일치로 판매 불가')
            return Response({'error': '소유한 차만 판매가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if not car.is_sold:
            logger.info(f'[{request.user}] - {car} - 판매되지 않은 차량으로 판매 불가')
            return Response({'error': '이 차량은 판매할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if UsedCarSales.objects.filter(car=car, user=request.user).exists():
            logger.info(f'[{request.user}] - {car} - 이미 판매 완료된 차량으로 판매 불가')
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
        logger.info(f'[{request.user}] - {car}:{discounted_price} - 차량 판매 완료')
        return Response({'message': 'Car sold', 'discounted_price': discounted_price}, status=status.HTTP_201_CREATED)


# 버전별 모든 자동차
class VersionAPI(generics.ListAPIView):
    permission_classes = []
    serializer_class = CustomVersionSerializer

    def get_queryset(self):
        versions = self.kwargs.get('versions')
        return Version.objects.filter(versions=versions)


# 자동차별 버전
class CarVersionsAPI(generics.ListAPIView):
    permission_classes = []
    serializer_class = VersionSerializer

    def get_queryset(self):
        car_brand = self.request.query_params.get('car_brand')
        answer = Version.objects.filter(car__brand=car_brand)

        if not answer.exists():
            raise NotFound(detail=f"Not found '{car_brand}'.")
        return answer
