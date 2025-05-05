from django.urls import path
from .views import DataCountView

urlpatterns = [
    path('data-count/', DataCountView.as_view(), name='data-count'),
]
