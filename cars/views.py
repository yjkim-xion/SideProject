from django.shortcuts import render

from rest_framework import generics
from rest_framework import mixins

from .models import Car
from .serializers import CarSerializer


# 자동차 전체 목록
class CarsListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# 자동차 디테일
class CarsDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.all().order_by('id')

    def get(self, request , *args , **kwargs):
        return self.retrieve(request, *args, **kwargs)
