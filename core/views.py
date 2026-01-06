from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, serializers
from drf_spectacular.utils import extend_schema
from .serializers import RegistrationSerializer, LoginSerializer
from .models import User, Order
from .utils import generate_jwt_token
from .permissions import RBCPermission
from .authentication import MiddlewareAuthentication  # <--- 1. ИМПОРТ


# --- AUTH VIEWS ---
# (RegisterView и LoginView остаются без изменений)
class RegisterView(APIView):

    @extend_schema(request=RegistrationSerializer, responses=None)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):


    @extend_schema(
        request=LoginSerializer,
        responses={200: None},  # (Опционально) говорим, что вернем токен
        description="Принимает email/password, возвращает JWT токен"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return Response({"error": "Account is disabled"}, status=status.HTTP_403_FORBIDDEN)

            if user.check_password(password):
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


# --- RESOURCE VIEWS (ORDER) ---

class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD для заказов.
    """
    # 2. ПОДКЛЮЧАЕМ НАШ МОСТИК
    authentication_classes = [MiddlewareAuthentication]

    serializer_class = OrderSerializer
    permission_classes = [RBCPermission]

    resource_code = 'orders'

    def get_queryset(self):
        queryset = Order.objects.all()
        scope = getattr(self.request, 'access_scope', None)
        if scope == 'ALL':
            return queryset
        elif scope == 'OWN':
            return queryset.filter(owner=self.request.user)
        else:
            return queryset.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)