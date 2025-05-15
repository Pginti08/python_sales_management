from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Country
from .serializers import CountrySerializer


class CountryListAPIView(APIView):
    """
    API View to list all countries with optional search via ?search=<query>.
    """

    def get(self, request):
        search_query = request.query_params.get('search', None)

        if search_query:
            countries = Country.objects.filter(
                Q(name__icontains=search_query) |
                Q(code__icontains=search_query)
            )
        else:
            countries = Country.objects.all()

        serializer = CountrySerializer(countries, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
