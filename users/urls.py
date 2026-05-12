from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView
)


app_name = UsersConfig.name
router = SimpleRouter()

urlpatterns = [
    # User CRUD
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("list/", UserListAPIView.as_view(), name="list"),
    path("<pk>/detail/", UserRetrieveAPIView.as_view(), name="detail"),
    path("<pk>/update/", UserUpdateAPIView.as_view(), name="update"),
    path("<pk>/delete/", UserDestroyAPIView.as_view(), name="delete"),
    # User Auth
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
] + router.urls  #type: ignore
