from django.urls import path
from .views import CountryListAPIView

urlpatterns = [
    path('countries/', CountryListAPIView.as_view(), name='country-list'),
]
