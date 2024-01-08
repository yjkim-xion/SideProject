from rest_framework.fields import SerializerMethodField
from .models import Car, CarSales, UsedCarSales, Version
from rest_framework import serializers


class VersionSerializer(serializers.ModelSerializer):
    added_features = serializers.StringRelatedField(many=True)
    removed_features = serializers.StringRelatedField(many=True)
    car_name = serializers.SerializerMethodField()
    car_brand = serializers.SerializerMethodField()

    class Meta:
        model = Version
        fields = ['car_name', 'car_brand', 'versions', 'added_features', 'removed_features', ]

    def get_car_name(self, obj):
        return obj.car.name

    def get_car_brand(self, obj):
        return obj.car.brand


class CustomVersionSerializer(VersionSerializer):
    car_name = serializers.SerializerMethodField()
    car_brand = serializers.SerializerMethodField()

    class Meta(VersionSerializer.Meta):
        fields = ['car_name', 'car_brand']

    def get_car_name(self, obj):
        return obj.car.name if obj.car else None

    def get_car_brand(self, obj):
        return obj.car.brand if obj.car else None


class CarSerializer(serializers.ModelSerializer):
    user = SerializerMethodField(read_only=True)
    versions = VersionSerializer(many=True, read_only=True, source='cars')

    class Meta:
        model = Car
        fields = ['name', 'brand', 'vin', 'price', 'versions', 'is_sold', 'user']

    def get_user(self, obj):
        if hasattr(obj, 'user'):
            from account.serializers import UserSerializer
            return UserSerializer(obj.user).data
        else:
            return None

    def create(self, validated_data):
        return CarSales.objects.create(**validated_data)


class CarSalesSerializer(serializers.ModelSerializer):
    sale_price = CarSerializer(read_only=True)
    versions = VersionSerializer(many=True, read_only=True, source='cars')

    class Meta:
        model = CarSales
        fields = ['car', 'sale_date', 'sale_price', 'versions']

    def create(self, validated_data):
        car = validated_data.get('car')

        if car.is_sold():
            raise serializers.ValidationError("이 자동차는 이미 판매 완료 되었습니다.")

        return CarSales.objects.create(**validated_data)


class UsedCarSalesSerializer(serializers.ModelSerializer):
    versions = VersionSerializer(many=True, read_only=True, source='cars')

    class Meta:
        model = UsedCarSales
        fields = ['car', 'sale_date', 'sale_price', 'discount_rate', 'versions']

    def create(self, validated_data):
        car = validated_data.get('car')

        if car.is_exists():
            raise serializers.ValidationError("이 자동차는 이미 판매되었습니다.")

        return UsedCarSales.objects.create(**validated_data)






