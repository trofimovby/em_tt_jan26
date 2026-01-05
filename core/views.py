from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer
from .models import User
from .utils import generate_jwt_token


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Ищем пользователя (вручную, без authenticate())
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            # Проверяем активность (мягкое удаление)
            if not user.is_active:
                return Response({"error": "Account is disabled"}, status=status.HTTP_403_FORBIDDEN)

            # Проверяем пароль через наш метод (bcrypt)
            if user.check_password(password):
                # Если всё ок — генерируем токен
                role_name = user.role.name if user.role else 'guest'
                token = generate_jwt_token(user.id, role_name)

                return Response({
                    "token": token,
                    "user_id": user.id,
                    "role": role_name
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)