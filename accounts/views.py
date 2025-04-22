from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category
from .serializers import (
    CategorySerializer,
    SignupSerializer,
    LoginSerializer,
    ProfileSerializer,
    LogoutSerializer
)

User = get_user_model()

# -----------------------------
# ✅ Category List & Create
# -----------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# -----------------------------
# ✅ Signup View
# -----------------------------
class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# ✅ Login View
# -----------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'data': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'id': user.id,
                    'email': user.email,
                    'name': user.name
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# -----------------------------
# ✅ Send Reset Email
# -----------------------------
class SendResetEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        reset_link = f"http://localhost:8000/reset-password-form?email={email}"

        send_mail(
            subject="Reset your password",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[user.email],
        )

        return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)


# -----------------------------
# ✅ Reset Password via Email
# -----------------------------
class ResetPasswordByEmailView(APIView):
    def post(self, request):
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


# -----------------------------
# ✅ Authenticated Password Change
# -----------------------------
class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get('password')
        if not new_password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


# -----------------------------
# ✅ Logout View
# -----------------------------
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------
# ✅ Sales User Profile View (Retrieve, Update, Delete)
# -----------------------------
class SalesUserProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
