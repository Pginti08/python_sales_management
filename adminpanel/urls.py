from django.urls import path
from .views import (
    AdminBankDetailListView,
    AdminBusinessDetailListView,
    AdminInvoiceListView,
    AdminClientListView,
    AdminProjectListView
)

urlpatterns = [
    path('banks/', AdminBankDetailListView.as_view(), name='admin-banks'),
    path('businesses/', AdminBusinessDetailListView.as_view(), name='admin-businesses'),
    path('invoices/', AdminInvoiceListView.as_view(), name='admin-invoices'),
    path('clients/', AdminClientListView.as_view(), name='admin-clients'),
    path('projects/', AdminProjectListView.as_view(), name='admin-projects'),

]
