from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import BankDetail
from .serializers import BankDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

class BankDetailListCreateView(generics.ListCreateAPIView):
    serializer_class = BankDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['bank_name']
    search_fields = ['bank_name', 'account_name']

    def get_queryset(self):
        if self.request.user.is_staff:
            return BankDetail.objects.all().order_by('-created_at')
        return BankDetail.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            # Admins cannot create bank details
            raise PermissionDenied("Admin users cannot create bank details.")
        serializer.save(user=self.request.user)


class BankDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BankDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            # Admin can access all records
            return BankDetail.objects.all()
        # Normal users only their own
        return BankDetail.objects.filter(user=self.request.user)
