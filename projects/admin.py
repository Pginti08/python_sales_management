from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'project_name', 'budget', 'start_date',
        'start_date_timestamp', 'end_date', 'end_date_timestamp',
        'status', 'client_selection', 'project_technology',
        'repo_links', 'developer_name', 'created_at', 'updated_at'
    )
    list_filter = ('status', 'project_technology', 'start_date', 'end_date')
    search_fields = ('project_name', 'developer_name', 'client_selection', 'repo_links')
    ordering = ('-created_at',)
