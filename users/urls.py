from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,

)


app_name = UsersConfig.name
router = SimpleRouter()

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),

] + router.urls  #type: ignore
