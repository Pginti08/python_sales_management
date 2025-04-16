from django.urls import path
from .views import BankDetailListCreateView, BankDetailRetrieveUpdateDestroyView

urlpatterns = [
    path('', BankDetailListCreateView.as_view(), name='bankdetail-list-create'),
    path('<int:pk>/', BankDetailRetrieveUpdateDestroyView.as_view(), name='bankdetail-detail'),
]
