from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'owner')
    list_display = ('id', 'name', 'owner', 'price')

