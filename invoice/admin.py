from django.contrib import admin
from .models import BusinessDetail, Invoice, InvoiceItem


@admin.register(Invoice)
class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'bank', 'client', 'business', 'country', 'invoice_number', 'invoice_date', 'status')
    search_fields = ('business_category', 'code')

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'name', 'quantity', 'price', 'gst', 'igst')
    search_fields = ('name', 'quantity', 'price')