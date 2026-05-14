from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Role


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


class UsersAccessAndDeleteTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_rbac')

    def setUp(self):
        self.admin_role = Role.objects.get(code=Role.ADMIN)
        self.manager_role = Role.objects.get(code=Role.MANAGER)
        self.user_role = Role.objects.get(code=Role.USER)

        self.admin = User.objects.create(
            email='admin@example.com',
            first_name='Admin',
            middle_name='',
            last_name='User',
            role=self.admin_role,
        )
        self.admin.set_password('testpass123')
        self.admin.save()

        self.manager = User.objects.create(
            email='manager@example.com',
            first_name='Manager',
            middle_name='',
            last_name='User',
            role=self.manager_role,
        )
        self.manager.set_password('testpass123')
        self.manager.save()

        self.user_1 = User.objects.create(
            email='user1@example.com',
            first_name='User',
            middle_name='',
            last_name='One',
            role=self.user_role,
        )
        self.user_1.set_password('testpass123')
        self.user_1.save()

        self.user_2 = User.objects.create(
            email='user2@example.com',
            first_name='User',
            middle_name='',
            last_name='Two',
            role=self.user_role,
        )
        self.user_2.set_password('testpass123')
        self.user_2.save()

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        return str(refresh)

    def test_user_cannot_retrieve_another_user(self):
        self.authenticate(self.user_1)

        response = self.client.get(reverse('users:detail', args=(self.user_2.id,)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_another_user(self):
        self.authenticate(self.user_1)

        response = self.client.patch(
            reverse('users:update', args=(self.user_2.id,)),
            {'first_name': 'Hacked'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_sees_all_users_in_list(self):
        self.authenticate(self.manager)

        response = self.client.get(reverse('users:list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], User.objects.count())

    def test_regular_user_sees_only_self_in_list(self):
        self.authenticate(self.user_1)

        response = self.client.get(reverse('users:list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.user_1.id)

    def test_soft_delete_blacklists_tokens_and_disables_login(self):
        refresh = self.authenticate(self.user_1)
        delete_url = reverse('users:delete', args=(self.user_1.id,))
        refresh_url = reverse('users:token_refresh')
        login_url = reverse('users:login')

        delete_response = self.client.delete(delete_url)
        refresh_response = self.client.post(refresh_url, {'refresh': refresh}, format='json')
        login_response = self.client.post(
            login_url,
            {'email': self.user_1.email, 'password': 'testpass123'},
            format='json',
        )

        self.user_1.refresh_from_db()

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user_1.is_active)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)
