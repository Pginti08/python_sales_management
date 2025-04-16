from django.contrib import admin
from .models import BankDetail

@admin.register(BankDetail)
class BankDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_name', 'bank_name', 'account_number', 'ifsc_code', 'swift_code')
    search_fields = ('account_name', 'bank_name', 'account_number', 'ifsc_code', 'swift_code')
