from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import os

class CustomDomainPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        # Get environment
        environment = os.environ.get('ENVIRONMENT', 'local')

        if environment == 'production':
            domain = 'https://api.vyzioninnovations.com'
        else:
            domain = 'http://localhost:8000'

        # Replace URLs in pagination response
        if response.data.get('next'):
            response.data['next'] = response.data['next'].replace(self.request.build_absolute_uri('/').rstrip('/'), domain)
        if response.data.get('previous'):
            response.data['previous'] = response.data['previous'].replace(self.request.build_absolute_uri('/').rstrip('/'), domain)

        return response
