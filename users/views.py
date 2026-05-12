from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserSerializer
from users.paginators import UsersPaginator


class UserCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = UsersPaginator


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
