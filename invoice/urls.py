# invoice/urls.py
from django.urls import path
from .views import InvoiceCreateView

urlpatterns = [
    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),
]
