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


class Version(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='cars')
    versions = models.IntegerField()
    added_features = models.JSONField(default=list)
    removed_features = models.JSONField(default=list)
    price = models.IntegerField(help_text='버전별 가격')

    #
    # def update_features(self):
    #     if self.versions == 1:
    #         self.added_features = ['핸들열선', '크루즈컨트롤']
    #         self.removed_features = []
    #
    #     elif self.versions == 2:
    #         self.added_features = ['자동주차']
    #         self.removed_features = ['핸들열선']
    #
    #     elif self.versions == 3:
    #         self.added_features = ['자율주행', '비행기모드']
    #         self.removed_features = ['크루즈컨트롤']

    # def save(self, *args, **kwargs):
    #     self.update_features()
    #     super().save(*args, **kwargs)

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

    def discount_price(self):  # 할인된 가격 생성
        discounted_price = self.sale_price * (1 - (self.discount_rate / 100))
        return int(discounted_price)

    def is_exists(self):
        return UsedCarSales.objects.filter(car=self).exists()
