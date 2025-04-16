from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import BankDetail
from .serializers import BankDetailSerializer

class BankDetailListCreateView(ListCreateAPIView):
    serializer_class = BankDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankDetail.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankDetailRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = BankDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankDetail.objects.filter(user=self.request.user)