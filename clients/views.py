from rest_framework import generics, permissions
from .models import Client
from .serializers import ClientSerializer

# List and Create clients for the logged-in user
class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only clients created by the current user
        return Client.objects.filter(user=self.request.user)

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
