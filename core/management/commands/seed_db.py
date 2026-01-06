from django.core.management.base import BaseCommand
from core.models import Role, Resource, Permission, User


class Command(BaseCommand):
    help = 'Наполняет БД начальными данными (Роли, Ресурсы, Тестовый админ)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем посев данных...")

        # 1. Создаем Роли
        admin_role, _ = Role.objects.get_or_create(name='admin', defaults={'description': 'Superuser'})
        user_role, _ = Role.objects.get_or_create(name='user', defaults={'description': 'Regular client'})

        self.stdout.write(self.style.SUCCESS(f'Роли созданы: {admin_role}, {user_role}'))

        # 2. Создаем Ресурс "orders"
        # Важно: code='orders' должен совпадать с resource_code в OrderViewSet (views.py)
        orders_resource, _ = Resource.objects.get_or_create(code='orders',
                                                            defaults={'description': 'Заказы пользователей'})

        self.stdout.write(self.style.SUCCESS(f'Ресурс создан: {orders_resource}'))

        # 3. Настраиваем Права (Permissions)

        # Админ: может ВСЁ
        Permission.objects.get_or_create(
            role=admin_role,
            resource=orders_resource,
            defaults={
                'can_create': True,
                'can_read_all': True,  # Видит всё
                'can_update_all': True,  # Правит всё
                'can_delete_all': True  # Удаляет всё
            }
        )

        # Обычный юзер: может создавать и видеть/править ТОЛЬКО СВОИ
        Permission.objects.get_or_create(
            role=user_role,
            resource=orders_resource,
            defaults={
                'can_create': True,
                'can_read_own': True,  # <-- Только свои
                'can_read_all': False,
                'can_update_own': True,  # <-- Только свои
                'can_update_all': False,
                'can_delete_own': False,
                'can_delete_all': False
            }
        )
        self.stdout.write(self.style.SUCCESS('Права доступа настроены'))

        # 4. Создаем пользователя-админа
        admin_email = 'admin@example.com'
        if not User.objects.filter(email=admin_email).exists():
            admin = User(
                first_name='Super',
                last_name='Admin',
                email=admin_email,
                role=admin_role
            )
            admin.set_password('admin123')  # Наш метод хеширования
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Пользователь создан: {admin_email} / admin123'))
        else:
            self.stdout.write(self.style.WARNING(f'Пользователь {admin_email} уже существует'))

        self.stdout.write(self.style.SUCCESS('Готово! База данных наполнена.'))
