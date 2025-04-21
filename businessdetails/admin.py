# common_country_module/admin.py

from django.contrib import admin
from .models import  BusinessDetail


@admin.register(BusinessDetail)
class BusinessDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'team_size', 'phone', 'country')
    search_fields = ('business_category', 'code')
