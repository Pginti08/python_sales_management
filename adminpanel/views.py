from django.core.mail import send_mail
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from accounts.models import SalesUser
from rest_framework.response import Response
from accounts.serializers import ProfileSerializer
from .serializers import (
    UserSerializer,
)

class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Admin can revoke or restore user access using custom actions.
    """
    queryset = SalesUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    # ========== REVOKE ACCESS ACTION ==========
    @action(methods=['post'], detail=True)
    def revoke_access(self, request, pk=None):
        """
        Custom action for Admin to revoke access of a Sales User.
        It disables the user's account (is_active=False) and sends an email notification.
        """
        user = self.get_object()
        user.is_active = False
        user.save()

        # Send email notification to user
        send_mail(
            subject="Your Account Access has been Revoked",
            message="Admin has revoked your account access.",
            from_email="admin@example.com",
            recipient_list=[user.email],
        )

        return Response({"detail": "Access revoked."}, status=status.HTTP_200_OK)
    # ========== END REVOKE ACCESS ACTION ==========

    # ========== RESTORE ACCESS ACTION ==========
    @action(methods=['post'], detail=True)
    def restore_access(self, request, pk=None):
        """
        Custom action for Admin to restore access of a Sales User.
        It enables the user's account (is_active=True) and sends an email notification.
        """
        user = self.get_object()
        user.is_active = True
        user.save()

        # Send email notification to user
        send_mail(
            subject="Your Account Access has been Restored",
            message="Admin has restored your account access.",
            from_email="admin@example.com",
            recipient_list=[user.email],
        )

        return Response({"detail": "Access restored."}, status=status.HTTP_200_OK)
    # ========== END RESTORE ACCESS ACTION ==========
