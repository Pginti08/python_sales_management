from django.db import models
from django.conf import settings
from django.utils import timezone  # Import timezone to set the default to now
from bankdetails.models import BankDetail
from businessdetails.models import BusinessDetail
from clients.models import Client
from common_country_module.models import Country


class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank = models.ForeignKey(BankDetail, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    business = models.ForeignKey(BusinessDetail, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    invoice_logo = models.ImageField(upload_to='invoices/logos/', default='unknown')
    created_at = models.DateTimeField(auto_now=True)  # auto_now_add is fine here
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    igst = models.DecimalField(max_digits=5, decimal_places=2)
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} (Invoice #{self.invoice.invoice_number})"
