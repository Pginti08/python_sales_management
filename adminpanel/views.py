from django.core.mail import send_mail
from rest_framework import filters, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import SalesUser
from accounts.serializers import ProfileSerializer  # ✅ added UserSerializer import from accounts.serializers
from clients import serializers
from common_country_module.models import Country
from .serializers import (
    BankDetailSerializer,
    BusinessDetailSerializer,
    InvoiceSerializer,
    ClientSerializer,
    ProjectSerializer,
    countrySerializer, UserSerializer, InvoiceItemSerializer
)
from bankdetails.models import BankDetail
from businessdetails.models import BusinessDetail
from invoice.models import Invoice, InvoiceItem
from clients.models import Client
from projects.models import Project


# ================== ADMIN BUSINESS DETAIL VIEWSET ==================
class AdminBusinessDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to view, create, update, and delete Business Details.
    Only accessible to Admin users.
    """
    queryset = BusinessDetail.objects.all().order_by('-created_at')
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.IsAdminUser]
# ================== END ADMIN BUSINESS DETAIL VIEWSET ==================


# ================== ADMIN INVOICE VIEWSET ==================
class AdminInvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to manage (CRUD) Invoices.
    Only accessible to Admin users.
    """
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAdminUser]
# ================== END ADMIN INVOICE VIEWSET ==================

class AdminInvoiceItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to manage (CRUD) Invoices.
    Only accessible to Admin users.
    """
    queryset = InvoiceItem.objects.all().order_by('-created_at')
    serializer_class = InvoiceItemSerializer
    permission_classes = [permissions.IsAdminUser]

# ================== ADMIN CLIENT VIEWSET ==================
class AdminClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to manage (CRUD) Clients.
    Only accessible to Admin users.
    """
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]
# ================== END ADMIN CLIENT VIEWSET ==================


# ================== ADMIN PROJECT VIEWSET ==================
class AdminProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to manage (CRUD) Projects.
    Only accessible to Admin users.
    """
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]
# ================== END ADMIN PROJECT VIEWSET ==================


# ================== ADMIN USER PROFILE VIEWSET ==================
class AdminUserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to view Sales Users' profiles.
    Only accessible to Admin users.
    """
    queryset = SalesUser.objects.all().order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]
# ================== END ADMIN USER PROFILE VIEWSET ==================


# ================== ADMIN BANK DETAIL VIEWSET ==================
class AdminBankDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admin to manage (CRUD) Bank Details.
    Only accessible to Admin users.
    """
    queryset = BankDetail.objects.all().order_by('-created_at')
    serializer_class = BankDetailSerializer
    permission_classes = [permissions.IsAdminUser]
# ================== END ADMIN BANK DETAIL VIEWSET ==================


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

#
# class AdminClientUserViewSet(viewsets.ModelViewSet):
#     queryset = Client.objects.all().order_by('-created_at')
#     serializer_class = ClientSerializer
#     permission_classes = [permissions.IsAdminUser]
#
#     @action(detail=False, methods=['get'])
#     def by_user(self, request):
#         user_id = request.query_params.get('user_id')
#         if not user_id:
#             return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
#         clients = Client.objects.filter(user_id=user_id)
#         serializer = self.get_serializer(clients, many=True)
#         return Response(serializer.data)
#
#     def perform_create(self, serializer):
#         user_id = self.request.data.get('user_id')
#         if not user_id:
#             raise serializers.ValidationError({'user_id': 'This field is required.'})
#         serializer.save(user_id=user_id)
#
# # ✅ ADMIN BUSINESS DETAIL VIEWSET (slight correction needed in exception raising)
# class AdminBusinessUserViewSet(viewsets.ModelViewSet):
#     queryset = BusinessDetail.objects.all().order_by('-created_at')
#     serializer_class = BusinessDetailSerializer
#     permission_classes = [permissions.IsAdminUser]
#
#     @action(detail=False, methods=['get'])
#     def by_user(self, request):
#         user_id = request.query_params.get('user_id')
#         if not user_id:
#             return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
#         businesses = BusinessDetail.objects.filter(user_id=user_id)
#         serializer = self.get_serializer(businesses, many=True)
#         return Response(serializer.data)
#
#     def perform_create(self, serializer):
#         user_id = self.request.data.get('user_id')
#         if not user_id:
#             raise serializers.ValidationError({'user_id': 'This field is required.'})
#         serializer.save(user_id=user_id)
#
