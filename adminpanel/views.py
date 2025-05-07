from rest_framework import generics, permissions, viewsets

from accounts.models import SalesUser
from accounts.serializers import ProfileSerializer
from .serializers import (
    BankDetailSerializer,
    BusinessDetailSerializer,
    InvoiceSerializer,
    ClientSerializer,
    ProjectSerializer
)
from bankdetails.models import BankDetail
from businessdetails.models import BusinessDetail
from invoice.models import Invoice
from clients.models import Client
from projects.models import Project

class AdminBusinessDetailViewSet(viewsets.ModelViewSet):
    queryset = BusinessDetail.objects.all().order_by('-created_at')
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminInvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminUserProfileViewSet(viewsets.ModelViewSet):
    queryset = SalesUser.objects.all().order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminBankDetailViewSet(viewsets.ModelViewSet):
    queryset = BankDetail.objects.all().order_by('-created_at')
    serializer_class = BankDetailSerializer
    permission_classes = [permissions.IsAdminUser]
