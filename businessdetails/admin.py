# common_country_module/admin.py

from django.contrib import admin
from .models import BusinessDetail, TeamSize


@admin.register(BusinessDetail)
class BusinessDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'business_name', 'team_size', 'phone', 'country', 'gstin')
    search_fields = ('business_category', 'code')

@admin.register(TeamSize)
class TeamSizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'id')
    search_fields = ('size', 'id')