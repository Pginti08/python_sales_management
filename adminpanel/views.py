from rest_framework import generics, permissions
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

class AdminBankDetailListView(generics.ListAPIView):
    queryset = BankDetail.objects.all().order_by('-created_at')
    serializer_class = BankDetailSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminBusinessDetailListView(generics.ListAPIView):
    queryset = BusinessDetail.objects.all().order_by('-created_at')
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminInvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminClientListView(generics.ListAPIView):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminProjectListView(generics.ListAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]
