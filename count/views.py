from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from bankdetails.models import BankDetail
from businessdetails.models import BusinessDetail
from invoice.models import Invoice
from clients.models import Client
from projects.models import Project

class DataCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        model_name = request.query_params.get('model', '').lower()

        model_mapping = {
            'bankdetail': BankDetail,
            'businessdetail': BusinessDetail,
            'invoice': Invoice,
            'client': Client,
            'project': Project,
        }

        model_class = model_mapping.get(model_name)

        if not model_class:
            return Response({'error': 'Invalid model name.'}, status=status.HTTP_400_BAD_REQUEST)

        # assuming all models have a 'user' ForeignKey field
        count = model_class.objects.filter(user=request.user).count()

        return Response({'module': model_name, 'count': count})
