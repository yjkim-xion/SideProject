from django.contrib import admin
from .models import Car, Version, Feature, CarSales, UsedCarSales


class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'vin', 'version', 'price', 'is_sold')
    search_fields = ('name', 'brand', 'vin')
    list_filter = ('brand', 'is_sold')


class VersionInline(admin.TabularInline):
    model = Version
    extra = 1


class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'vin', 'version', 'price', 'is_sold')
    inlines = [VersionInline]


class VersionAdmin(admin.ModelAdmin):
    list_display = ('car', 'version_number', 'display_added_features', 'display_removed_features')

    def display_added_features(self, obj):
        return ", ".join([feature.name for feature in obj.added_features.all()])
    display_added_features.short_description = 'Added Features'

    def display_removed_features(self, obj):
        return ", ".join([feature.name for feature in obj.removed_features.all()])
    display_removed_features.short_description = 'Removed Features'


admin.site.register(Car)
admin.site.register(Version)
admin.site.register(Feature)
admin.site.register(CarSales)
admin.site.register(UsedCarSales)
