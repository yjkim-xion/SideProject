from cars.serializers import VersionSerializer
from .models import User
from rest_framework import serializers
from cars.models import CarSales, UsedCarSales
from rest_framework.fields import SerializerMethodField


class UserSerializer(serializers.ModelSerializer):
    purchased_cars = SerializerMethodField(read_only=True)
    sold_cars = SerializerMethodField(read_only=True)
    # versions = VersionSerializer(many=True, read_only=True, source='cars')

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    def get_purchased_cars(self, obj):
        purchased = CarSales.objects.filter(user=obj).select_related('car')
        return [{'brand': sale.car.brand, 'car': sale.car.name, 'price': str(sale.sale_price) + '만원', 'sale_date': sale.sale_date,
                } for sale in
                purchased]

    def get_sold_cars(self, obj):
        sold = UsedCarSales.objects.filter(user=obj).select_related('car')
        return [{'brand': sale.car.brand, 'car': sale.car.name, 'price': str(sale.sale_price) + '만원', 'sale_date': sale.sale_date,
                } for sale in sold]
