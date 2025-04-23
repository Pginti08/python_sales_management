from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'business_name', 'phone', 'client_type', 'country']
    ordering = ['email']
    search_fields = ['email', 'business_name', 'phone']
    list_filter = ['country', 'client_type']

    fieldsets = (
        (None, {
            'fields': ('user', 'email', 'business_name', 'phone', 'country', 'city_town', 'client_type', 'gstin', 'pan')
        }),
    )
