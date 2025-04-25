from django.urls import path
from .views import (
    InvoiceCreateView,
    InvoiceDetailView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    InvoiceListView,
)

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoices/<int:invoice_id>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/update/<int:invoice_id>/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('invoices/delete/<int:invoice_id>/', InvoiceDeleteView.as_view(), name='invoice-delete'),
]
