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
    password_hash = models.CharField(max_length=255)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        self.password_hash = hashed.decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def __str__(self):
        return self.email


# 4. Таблица прав доступа
class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='permissions')

    can_create = models.BooleanField(default=False)

    can_read_own = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)

    can_update_own = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)

    can_delete_own = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'resource')


# 5. Тестовая сущность "Заказ" (ВОТ ЕЁ НЕ ХВАТАЛО)
class Order(models.Model):
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.owner.email}"