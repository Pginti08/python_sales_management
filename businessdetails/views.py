from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from businessdetails.models import BusinessDetail, TeamSize
from businessdetails.serializers import BusinessDetailSerializer, TeamSizeSerializer
from accounts.models import SalesUser  # replace this with your actual user model

@csrf_exempt
@api_view(['GET', 'POST'])
def team_size_create(request):
    if request.method == 'GET':
        categories = TeamSize.objects.all().order_by('-created_at')
        serializer = TeamSizeSerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ✅ BusinessDetail list & create view
class BusinessDetailListCreateView(generics.ListCreateAPIView):
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['country', 'state']
    search_fields = ['business_name', 'phone']

    def get_queryset(self):
        if self.request.user.is_staff:
            return BusinessDetail.objects.all().order_by('-created_at')
        return BusinessDetail.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            # Admins cannot create bank details
            raise PermissionDenied("Admin users cannot create Business details.")
        serializer.save(user=self.request.user)


# ✅ BusinessDetail retrieve/update/delete view

class BusinessDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BusinessDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return BusinessDetail.objects.all()
        return BusinessDetail.objects.filter(user=self.request.user)
