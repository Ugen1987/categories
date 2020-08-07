from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    pass


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Sale)
class SaleModelAdmin(admin.ModelAdmin):
    pass

