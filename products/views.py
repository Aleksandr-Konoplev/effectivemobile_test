from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from products.permissions import IsProductOwnerOrReadOnly
from products.serializers import ProductSerializer


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsProductOwnerOrReadOnly)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDestroyAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsProductOwnerOrReadOnly)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

