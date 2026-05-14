from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from users.models import User
from users.serializers import UserSerializer, LogoutSerializer
from users.paginators import UsersPaginator
from users.permissions import HasUserAccessPermission


class UserCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save(is_active=True)


class UserListAPIView(ListAPIView):
    permission_classes = (HasUserAccessPermission,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = UsersPaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()

        role = getattr(user, 'role', None)
        if role and role.code in ('admin', 'manager'):
            return User.objects.all()

        return User.objects.filter(pk=user.pk)


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = (HasUserAccessPermission,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = (HasUserAccessPermission,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, HasUserAccessPermission)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        tokens = OutstandingToken.objects.filter(user=instance)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        instance.is_active = False
        instance.save()


class LogoutAPIView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
