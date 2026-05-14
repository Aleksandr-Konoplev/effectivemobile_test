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
    path('<int:pk>/detail/', ProductRetrieveAPIView.as_view(), name='retrieve'),
    path('<int:pk>/update/', ProductUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', ProductDestroyAPIView.as_view(), name='destroy'),
] + router.urls  #type: ignore
