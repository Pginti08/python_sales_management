from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer

class CountryListAPIView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response({'data': serializer.data})
