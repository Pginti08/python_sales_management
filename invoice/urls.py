from django.urls import path
from .views import InvoiceCreateView, InvoiceDetailView

urlpatterns = [
    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),  # for POST
    path('<str:invoice_number>/', InvoiceDetailView.as_view(), name='invoice-detail'),  # for GET
]
