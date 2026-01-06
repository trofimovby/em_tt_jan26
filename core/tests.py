from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Role, Resource, Permission, Order


class OrderFlowTests(APITestCase):
    def setUp(self):
        # 1. Подготовка данных (аналог seed_db, но для теста)
        self.admin_role = Role.objects.create(name='admin')
        self.resource = Resource.objects.create(code='orders')

        # Даем права админу
        Permission.objects.create(
            role=self.admin_role,
            resource=self.resource,
            can_create=True,
            can_read_own=True
        )

        # Создаем юзера
        self.email = 'test@example.com'
        self.password = 'password123'
        self.user = User(email=self.email, role=self.admin_role)
        self.user.set_password(self.password)
        self.user.save()

        # URL-адреса
        self.login_url = reverse('login')
        # Для ViewSet URL строится как 'basename-action'
        self.orders_list_url = reverse('orders-list')

    def test_full_order_cycle(self):
        """
        Тест полного цикла: Логин -> Получение Токена -> Создание Заказа
        """
        # Шаг 1: Логин
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data.get('token')
        self.assertTrue(token, "Токен не пришел в ответе!")

        # Шаг 2: Создание заказа с токеном
        # В тестах DRF токен передается через credentials
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        order_data = {'description': 'AutoTest Order'}
        response = self.client.post(self.orders_list_url, order_data)

        # Проверяем, что заказ создан (201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'AutoTest Order')
        self.assertEqual(response.data['owner'], self.email)

        # Проверяем, что он реально есть в базе
        self.assertEqual(Order.objects.count(), 1)
        print("\n✅ Тест полного цикла прошел успешно!")

    def test_access_denied_without_token(self):
        """
        Проверка защиты: без токена доступ запрещен
        """
        response = self.client.post(self.orders_list_url, {'description': 'Hacker Order'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\n✅ Тест защиты прошел успешно!")