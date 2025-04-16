# Importing generic views and permission classes from DRF
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import IntegrityError

# Importing the BusinessDetail model and its serializer
from businessdetails.models import BusinessDetail, TeamSize
from businessdetails.serializers import BusinessDetailSerializer, TeamSizeSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
def team_size_create(request):
    if request.method == 'GET':
        categories = TeamSize.objects.all()
        serializer = TeamSizeSerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class BusinessDetailListCreateView(generics.ListCreateAPIView):
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessDetail.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
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
