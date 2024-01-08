from django.urls import path
from .views import CarsListAPI, CarsDetailAPI, PurchaseCarAPI,SellUsedCarAPI, ReturnCarAPI,VersionAPI,CarVersionsAPI

app_name = 'cars'

urlpatterns = [
    path('carlist/', CarsListAPI.as_view(), name='carList'),
    path('carsdetail/<int:pk>/', CarsDetailAPI.as_view(), name='carsDetail'),
    path('purchase/', PurchaseCarAPI.as_view(), name='purchases'),
    path('sellcars/', SellUsedCarAPI.as_view(), name='sellcars'),
    path('returncar/', ReturnCarAPI.as_view(), name='returnCar'),
    path('version_car/<int:versions>/', VersionAPI.as_view(), name='versionCar'),
    path('car_version/', CarVersionsAPI.as_view(), name='carVersion'),
]
