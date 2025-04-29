from rest_framework import generics, permissions, filters
from .models import Client
from .serializers import ClientSerializer
from django_filters.rest_framework import DjangoFilterBackend


# List and Create clients for the logged-in user
class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # Fields you want to allow filtering
    filterset_fields = ['client_region', 'client_type']  # example fields, you can customize
    # Fields you want to allow searching
    search_fields = ['business_name', 'phone']  # example fields, you can customize

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically assign the logged-in user
        serializer.save(user=self.request.user)

# Retrieve, Update, Delete a single client of the logged-in user
class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Make sure users can only access their own clients
        return Client.objects.filter(user=self.request.user)


