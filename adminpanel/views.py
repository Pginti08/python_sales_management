from django.core.mail import send_mail
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from accounts.models import SalesUser

from bankdetails.models import BankDetail
from businessdetails.models import BusinessDetail
from invoice.models import Invoice, InvoiceItem
from clients.models import Client
from projects.models import Project
from rest_framework.response import Response

from accounts.serializers import ProfileSerializer
from .serializers import (
    BankDetailSerializer,
    BusinessDetailSerializer,
     ClientSerializer,
    ProjectSerializer, UserSerializer,
)


# ================== BASE ADMIN VIEWSET ==================
class AdminBaseUserLinkedViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for models linked to SalesUser (user field).
    Admin can perform full CRUD and assign user_id during creation.
    """
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        if not user_id:
            raise ValidationError({'user_id': 'This field is required to create the record.'})

        try:
            user = SalesUser.objects.get(id=user_id)
        except SalesUser.DoesNotExist:
            raise ValidationError({'user_id': f'SalesUser with id={user_id} does not exist.'})

        serializer.save(user=user)


# ================== VIEWSETS USING BASE WITH USER ==================
class AdminClientViewSet(AdminBaseUserLinkedViewSet):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer


class AdminProjectViewSet(AdminBaseUserLinkedViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer


class AdminBankDetailViewSet(AdminBaseUserLinkedViewSet):
    queryset = BankDetail.objects.all().order_by('-created_at')
    serializer_class = BankDetailSerializer


class AdminBusinessDetailViewSet(AdminBaseUserLinkedViewSet):
    queryset = BusinessDetail.objects.all().order_by('-created_at')
    serializer_class = BusinessDetailSerializer


# ================== ADMIN USER VIEWSET ==================


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to manage Sales Users.
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
