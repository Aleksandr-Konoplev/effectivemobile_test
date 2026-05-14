from decimal import Decimal

from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from products.models import Product
from users.models import Role, User


class ProductRBACTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_rbac')

    def setUp(self):
        self.admin_role = Role.objects.get(code=Role.ADMIN)
        self.manager_role = Role.objects.get(code=Role.MANAGER)
        self.user_role = Role.objects.get(code=Role.USER)

        self.admin = User.objects.create(
            email='admin_prod@example.com',
            first_name='Admin',
            middle_name='',
            last_name='Prod',
            role=self.admin_role,
        )
        self.admin.set_password('testpass123')
        self.admin.save()

        self.manager = User.objects.create(
            email='manager_prod@example.com',
            first_name='Manager',
            middle_name='',
            last_name='Prod',
            role=self.manager_role,
        )
        self.manager.set_password('testpass123')
        self.manager.save()

        self.user_1 = User.objects.create(
            email='user1_prod@example.com',
            first_name='User',
            middle_name='',
            last_name='One',
            role=self.user_role,
        )
        self.user_1.set_password('testpass123')
        self.user_1.save()

        self.user_2 = User.objects.create(
            email='user2_prod@example.com',
            first_name='User',
            middle_name='',
            last_name='Two',
            role=self.user_role,
        )
        self.user_2.set_password('testpass123')
        self.user_2.save()

        self.product_1 = Product.objects.create(
            name='Product 1',
            description='Test',
            price=Decimal('100.00'),
            owner=self.user_1,
        )
        self.product_2 = Product.objects.create(
            name='Product 2',
            description='Test',
            price=Decimal('200.00'),
            owner=self.user_2,
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_guest_can_read_products(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_guest_cannot_create_product(self):
        response = self.client.post(
            reverse('products:create'),
            {'name': 'New', 'description': 'Desc', 'price': '10.00'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_update_own_product(self):
        self.authenticate(self.user_1)

        response = self.client.patch(
            reverse('products:update', args=(self.product_1.id,)),
            {'name': 'Updated name'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_foreign_product(self):
        self.authenticate(self.user_1)

        response = self.client.patch(
            reverse('products:update', args=(self.product_2.id,)),
            {'name': 'Updated name'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cannot_delete_products(self):
        self.authenticate(self.manager)

        response = self.client.delete(reverse('products:destroy', args=(self.product_1.id,)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_product(self):
        self.authenticate(self.admin)

        response = self.client.delete(reverse('products:destroy', args=(self.product_1.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
