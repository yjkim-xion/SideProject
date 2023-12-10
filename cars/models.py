from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    base_price = models.IntegerField()

    def __str__(self):
        return self.name


class Version(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    added_features = models.TextField()
    removed_features = models.TextField(null=True)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.car.name} - ver. {self.version_number}"


class CarSales(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='sales')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    sale_date = models.DateField()
    sale_price = models.IntegerField()


class UsedCarSales(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='used_sales')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='used_purchases')
    sale_date = models.DateField()
    sale_price = models.IntegerField()
    discount_rate = models.IntegerField()

    def discount_price(self):
        discounted_price = self.sale_price * (1 - (self.discount_rate / 100))
        return int(discounted_price)

