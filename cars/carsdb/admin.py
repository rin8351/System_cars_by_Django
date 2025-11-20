from django.contrib import admin
from .models import parts, cars, car_part

# Register your models here.

@admin.register(parts)
class PartsAdmin(admin.ModelAdmin):
    list_display = ('model_p', 'type', 'price', 'count_p', 'params')
    search_fields = ('model_p', 'type')
    list_filter = ('type',)

@admin.register(cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('name', 'margin', 'price')
    search_fields = ('name',)
    filter_horizontal = ('parts',)

@admin.register(car_part)
class CarPartAdmin(admin.ModelAdmin):
    list_display = ('car', 'part', 'name')
    search_fields = ('car__name', 'part__model_p')
    list_filter = ('car',)
