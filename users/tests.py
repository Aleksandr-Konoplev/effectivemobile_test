from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class LogoutAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='user@example.com',
            first_name='Test',
            middle_name='',
            last_name='User',
        )
        self.user.set_password('testpass123')
        self.user.save()
        self.logout_url = reverse('users:logout')
        self.refresh_url = reverse('users:token_refresh')

    def make_refresh_token(self):
        return str(RefreshToken.for_user(self.user))

    def logout(self, refresh):
        return self.client.post(self.logout_url, {'refresh': refresh}, format='json')

    def refresh_access(self, refresh):
        return self.client.post(self.refresh_url, {'refresh': refresh}, format='json')

    def test_logout_blacklists_refresh_token(self):
        refresh = self.make_refresh_token()

        response = self.logout(refresh)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_rejects_blacklisted_refresh_token(self):
        refresh = self.make_refresh_token()

        first_response = self.logout(refresh)
        second_response = self.logout(refresh)

        self.assertEqual(first_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(second_response.json(), {'refresh': ['Токен невалидный, или срок действия истек']})

    def test_refresh_token_cannot_be_used_after_logout(self):
        refresh = self.make_refresh_token()

        logout_response = self.logout(refresh)
        refresh_response = self.refresh_access(refresh)

        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)