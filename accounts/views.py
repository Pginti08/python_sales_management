from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CategorySerializer, SignupSerializer, LoginSerializer  # make sure this exists

@csrf_exempt
@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def signup_view(request):
    """User signup view with validation."""
    serializer = SignupSerializer(data=request.data)  #
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """User login view that returns JWT tokens."""
    serializer = LoginSerializer(data=request.data)  # ✅ Use request.data
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'id': user.id,
                'email': user.email,
                'name': user.name
                          }
        })
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


User = get_user_model()
@api_view(['POST'])
def send_reset_email(request):
    """Send reset password link via email (no token)."""
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Simple link with email query (not secure in public systems)
    reset_link = f"http://localhost:8000/reset-password-form?email={email}"

    send_mail(
        subject="Reset your password",
        message=f"Click the link to reset your password: {reset_link}",
        from_email=None,
        recipient_list=[user.email],
    )

    return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password_by_email(request):
    """Reset password using just email."""
    email = request.data.get('email')
    new_password = request.data.get('password')

    if not email or not new_password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get('password')

        if not new_password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user  # 🧠 automatically fetched from token
        user.set_password(new_password)  # 🔐 hash and set password
        user.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)