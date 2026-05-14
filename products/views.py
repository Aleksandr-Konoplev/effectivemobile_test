from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from products.models import Product
from products.permissions import HasProductPermission
from products.serializers import ProductSerializer


class ProductCreateAPIView(CreateAPIView):
    permission_classes = (HasProductPermission,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductListAPIView(ListAPIView):
    permission_classes = (HasProductPermission,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductRetrieveAPIView(RetrieveAPIView):
    permission_classes = (HasProductPermission,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductUpdateAPIView(UpdateAPIView):
    permission_classes = (HasProductPermission,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDestroyAPIView(DestroyAPIView):
    permission_classes = (HasProductPermission,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

