from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import os

class CustomDomainPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.request = request  # ✅ STORE request
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        environment = os.environ.get('ENVIRONMENT', 'local')

        if environment == 'production':
            domain = 'https://api.vyzioninnovations.com'
        else:
            domain = 'http://localhost:8000'

        current_host = self.request.build_absolute_uri('/').rstrip('/')

        if response.data.get('next'):
            response.data['next'] = response.data['next'].replace(current_host, domain)
        if response.data.get('previous'):
            response.data['previous'] = response.data['previous'].replace(current_host, domain)

        return response
