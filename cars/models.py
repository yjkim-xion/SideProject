from django.db import models
from django.conf import settings
from account.models import User


class Car(models.Model):
    name = models.CharField(help_text='차 이름', max_length=100)
    brand = models.CharField(help_text='차 브랜드', max_length=100)
    vin = models.CharField(help_text='식별변호', max_length=10, unique=True)
    version = models.IntegerField(help_text='버전')
    price = models.IntegerField(help_text='가격')
    is_sold = models.BooleanField(default=False, null=False)
    features = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    def is_car_sold(self):
        return CarSales.objects.filter(car=self).exists()

    def add_feature(self, feature_name):
        self.features[feature_name] = {"added": True, "removed": False}

    def remove_feature(self, feature_name):
        if feature_name in self.features:
            self.features[feature_name]["added"] = False
            self.features[feature_name]["removed"] = True

    def has_feature(self, feature_name):
        return self.features.get(feature_name, {"added": False, "removed": False})

    def update_features_version(self):
        if self.version == 1:
            self.add_feature('핸들열선')
            self.add_feature('크루즈컨트롤')
        elif self.version == 2:
            self.add_feature('자동주차')
            self.remove_feature('핸들열선')
        else:
            self.add_feature('자율주행')
            self.add_feature('비행기모드')
            self.remove_feature('크루즈컨트롤')

    def save(self, *args, **kwargs):
        self.update_features_version()
        super().save(*args, **kwargs)


# class Version(models.Model):
#     versions = {
#         ('버전선택','버전선택'),
#         ('1','버전1'),
#         ('2','버전2'),
#         ('3','버전3'),
#     }
#     car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars')
#     versions = models.CharField(max_length=80, choices=versions, default='버전선택')
#     added_features = models.TextField(null=True, blank=True)
#     removed_features = models.TextField(null=True, blank=True)
#     price = models.IntegerField(help_text='버전별 가격')
#
#     def __str__(self):
#         return f"{self.car.name} - ver.{self.versions}"


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

    def discount_price(self):  # 할인된 가격 생성
        discounted_price = self.sale_price * (1 - (self.discount_rate / 100))
        return int(discounted_price)

    def is_exists(self):
        return UsedCarSales.objects.filter(car=self).exists()
