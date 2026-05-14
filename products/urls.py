from django.urls import path
from rest_framework.routers import SimpleRouter

from products.apps import ProductsConfig
from products.views import (
    ProductCreateAPIView,
    ProductListAPIView,
    ProductRetrieveAPIView,
    ProductUpdateAPIView,
    ProductDestroyAPIView
)


app_name = ProductsConfig.name
router = SimpleRouter()

urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name='create'),
    path('list/', ProductListAPIView.as_view(), name='list'),
    path('retrieve/<int:pk>/', ProductRetrieveAPIView.as_view(), name='retrieve'),
    path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name='update'),
    path('destroy/<int:pk>/', ProductDestroyAPIView.as_view(), name='destroy'),
] + router.urls  #type: ignore
