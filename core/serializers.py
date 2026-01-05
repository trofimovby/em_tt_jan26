from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    # Поля для ввода пароля (write_only - чтобы API не отдавал их обратно)
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, data):
        # Проверка: совпадают ли пароли
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Удаляем повтор пароля из данных
        validated_data.pop('password_repeat')
        password = validated_data.pop('password')

        # Создаем инстанс, но пока не сохраняем
        user = User(**validated_data)

        # Хешируем пароль через наш метод в модели
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)