from django.contrib import admin
from .models import SalesUser, Category
from django.contrib.auth.admin import UserAdmin

class SalesUserAdmin(UserAdmin):
    model = SalesUser




    list_display = ['email', 'name', 'phone', 'is_staff', 'role']
    ordering = ['email']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'phone')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'password1', 'password2', 'category', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Show both ID and name

admin.site.register(SalesUser, SalesUserAdmin)
admin.site.register(Category, CategoryAdmin)
