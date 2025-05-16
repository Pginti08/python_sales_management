from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client
from .serializers import ClientSerializer
from accounts.models import SalesUser  # Import the user model used in your system


# ✅ List and Create Clients (admin or normal user)
class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Enable filtering on these fields
    filterset_fields = ['client_region', 'client_type']
    # Enable searching on these fields
    search_fields = ['business_name', 'phone']

    # Get client list
    def get_queryset(self):
        # ✅ If admin, return all clients
        if self.request.user.is_staff:
            return Client.objects.all().order_by('-created_at')
        # ✅ If normal user, return only their own clients
        return Client.objects.filter(user=self.request.user).order_by('-created_at')

    # Create a new client
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            raise PermissionError("Admins are not allowed to create clients.")
        serializer.save(user=self.request.user)


# ✅ Retrieve, Update, and Delete a specific client
class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)




