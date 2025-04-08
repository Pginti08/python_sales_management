from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SalesUser, Category

class SalesUserAdmin(UserAdmin):
    model = SalesUser
    list_display = ['email', 'username', 'name', 'phone', 'category', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'phone', 'category')}),
    )

admin.site.register(SalesUser, SalesUserAdmin)
admin.site.register(Category)
