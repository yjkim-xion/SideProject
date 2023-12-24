from django.db import models
from django.conf import settings
from account.models import User


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(help_text='차 이름', max_length=100)
    brand = models.CharField(help_text='차 브랜드', max_length=100)
    vin = models.CharField(help_text='식별변호', max_length=10, unique=True)
    price = models.IntegerField(help_text='가격')
    is_sold = models.BooleanField(default=False, null=False)
    features = models.ManyToManyField(Feature, related_name='cars')

    def __str__(self):
        return self.name

    def is_car_sold(self):
        return CarSales.objects.filter(car=self).exists()


class Version(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars')
    versions = models.IntegerField()
    added_features = models.ManyToManyField(Feature, related_name='added_to_versions')
    removed_features = models.ManyToManyField(Feature, related_name='removed_from_versions')
    price = models.IntegerField(help_text='버전별 가격')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.added_features.clear()
        self.removed_features.clear()

        if self.versions == 1:
            feature1 = Feature.objects.get_or_create(name='핸들열선')
            feature2 = Feature.objects.get_or_create(name='크루즈컨트롤')
            self.added_features.add(feature1, feature2)

        elif self.versions == 2:
            feature3 = Feature.objects.get_or_create(name='자동주차')
            feature1 = Feature.objects.get_or_create(name='핸들열선')
            self.added_features.add(feature3)
            self.removed_features.add(feature1)

        elif self.versions == 3:
            feature4 = Feature.objects.get_or_create(name='자율주행')
            feature5 = Feature.objects.get_or_create(name='비행기모드')
            feature2 = Feature.objects.get_or_create(name='크루즈컨트롤')
            self.added_features.add(feature4, feature5)
            self.removed_features.add(feature2)

    def __str__(self):
        return f"{self.car.name} - ver.{self.versions}"


class CarSales(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='sales')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    sale_date = models.DateTimeField(auto_now_add=True)
    sale_price = models.IntegerField(help_text='구매 가격')


class UsedCarSales(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='used_sales')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='used_purchases')
    sale_date = models.DateTimeField(auto_now_add=True)
    sale_price = models.IntegerField()
    discount_rate = models.IntegerField()

    def is_exists(self):
        return UsedCarSales.objects.filter(car=self).exists()
