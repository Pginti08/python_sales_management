from django.urls import path
from .views import BankDetailListCreateView, BankDetailRetrieveUpdateDestroyView

urlpatterns = [
    path('bankdetails/', BankDetailListCreateView.as_view(), name='bankdetail-list-create'),
    path('bankdetails/<int:pk>/', BankDetailRetrieveUpdateDestroyView.as_view(), name='bankdetail-detail'),
]
