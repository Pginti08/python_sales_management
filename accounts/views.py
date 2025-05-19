from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .serializers import (
    CategorySerializer,
    SignupSerializer,
    LoginSerializer,
    ProfileSerializer
)

User = get_user_model()

# -----------------------------
# ✅ Signup View (Refactored)
# -----------------------------
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)


# -----------------------------
# ✅ Login View (JWT based)
# -----------------------------
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'id': user.id,
            'email': user.email,
            'name': user.name
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# -----------------------------
# ✅ Logout View (Clears client-side tokens only)
# -----------------------------
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Token successfully blacklisted."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# ✅ Category List & Create
# -----------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# -----------------------------
# ✅ Send Password Reset Email
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

        reset_link = f"https://api.vyzioninnovations.com/reset-password-form?email={email}"

        send_mail(
            subject="Reset your password",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[user.email],
        )

        return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)


# -----------------------------
# ✅ Reset Password via Email (No login required)
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
# ✅ Change Password (Authenticated)
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
# ✅ Profile View (Retrieve, Update, Delete)
# -----------------------------

class AdminUserListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can access
    queryset = User.objects.all()


class SalesUserProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        # Admins can access all users
        if self.request.user.is_staff:
            return User.objects.all()
        # Normal users can only access their own data
        return User.objects.filter(pk=self.request.user.pk)

class SelfUserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class AdminUserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    lookup_field = 'pk'
