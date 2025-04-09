# Importing generic views and permission classes from DRF
from rest_framework import generics, permissions

# Importing the BusinessDetail model and its serializer
from businessdetails.models import BusinessDetail
from businessdetails.serializers import BusinessDetailSerializer


class BusinessDetailListCreateView(generics.ListCreateAPIView):
    # Serializer used to convert model instances to JSON and vice versa
    serializer_class = BusinessDetailSerializer

    permission_classes = [permissions.IsAuthenticated]

    # Define the queryset (what data to show)
    def get_queryset(self):
        # Only return the business details for the currently logged-in user
        return BusinessDetail.objects.filter(user=self.request.user)

    # Define what happens when creating a new BusinessDetail (POST request)
    def perform_create(self, serializer):
        # Automatically assign the currently logged-in user to the user field
        serializer.save(user=self.request.user)


# -----------------------------
# ✅ View to Retrieve, Update, and Delete Business Detail by ID
# -----------------------------
class BusinessDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # Use the same serializer
    serializer_class = BusinessDetailSerializer

    # Only logged-in users can access this view
    permission_classes = [permissions.IsAuthenticated]

    # Again, filter the queryset so users can only access their own data
    def get_queryset(self):
        return BusinessDetail.objects.filter(user=self.request.user)
