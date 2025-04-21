from django.contrib import admin

from products.models import Product


@admin.register(Product)
class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'igst', 'business')
    search_fields = ('amount', 'code')
