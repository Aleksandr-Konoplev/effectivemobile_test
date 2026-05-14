from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'owner')
