from rest_framework.permissions import IsAuthenticated
from .models import BankDetail
from .serializers import BankDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

class BankDetailListCreateView(generics.ListCreateAPIView):
    serializer_class = BankDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Fields you want to allow filtering
    filterset_fields = ['bank_name']  # example fields, you can customize
    # Fields you want to allow searching
    search_fields = ['bank_name', 'account_name']  # example fields, you can customize

    def get_queryset(self):
        return BankDetail.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BankDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankDetail.objects.filter(user=self.request.user)