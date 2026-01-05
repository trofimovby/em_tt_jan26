from django.db import models
import bcrypt


# 1. Справочник Ролей (Admin, Manager, User)
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# 2. Справочник Ресурсов (Orders, Profile, Products)
class Resource(models.Model):
    code = models.CharField(max_length=50, unique=True)  # например "orders"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


# 3. Наш кастомный Пользователь
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    # Храним не пароль, а хеш. Max_length побольше, т.к. хеши длинные
    password_hash = models.CharField(max_length=255)

    # Связь с ролью (если роль удалят, юзер останется без роли - SET_NULL)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')

    # Мягкое удаление
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Метод для установки пароля (инкапсулируем логику bcrypt здесь)
    def set_password(self, raw_password):
        # bcrypt требует байты, поэтому encode. salt генерируется сама.
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        self.password_hash = hashed.decode('utf-8')

    # Метод проверки пароля
    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def __str__(self):
        return self.email


# 4. Таблица прав доступа (Матрица доступа)
class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='permissions')

    # CRUD + Scope (свои/все)
    # Create
    can_create = models.BooleanField(default=False)

    # Read
    can_read_own = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)

    # Update
    can_update_own = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)

    # Delete
    can_delete_own = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        # Уникальность: у одной роли к одному ресурсу может быть только 1 запись с правилами
        unique_together = ('role', 'resource')