from django.db import models
from django.conf import settings


class Car(models.Model):
    name = models.CharField(help_text='차 이름', max_length=100)
    brand = models.CharField(help_text='차 브랜드', max_length=100)
    vin = models.CharField(help_text='식별변호', max_length=10, unique=True)
    version = models.IntegerField(help_text='버전')
    price = models.IntegerField(help_text='가격')

    def __str__(self):
        return self.name


class Version(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='versions')
    version_number = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='versions_num')
    added_features = models.TextField(null=True)
    removed_features = models.TextField(null=True)
    price = models.IntegerField(help_text='버전별 가격')

    def __str__(self):
        return f"{self.car.name} - ver. {self.version_number}"


class CarSales(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='sales')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    sale_date = models.DateField()
    sale_price = models.IntegerField()


class UsedCarSales(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='used_sales')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='used_purchases')
    sale_date = models.DateField()
    sale_price = models.IntegerField()
    discount_rate = models.IntegerField()

    # noinspection PyTypeChecker
    def discount_price(self):  # 할인된 가격 생성
        discounted_price = self.sale_price * (1 - (self.discount_rate / 100))
        return int(discounted_price)

