from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):



class UserListAPIView(ListAPIView):
    pass


class UserRetrieveUpdateAPIView(RetrieveAPIView):
    pass


class UserUpdateAPIView(UpdateAPIView):
    pass


class UserDestroyAPIView(DestroyAPIView):
    pass
