from django.db import models
from django.conf import settings
from clients.models import Client
from common_country_module.models import Country


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    start_date_timestamp = models.BigIntegerField(blank=True, null=True)
    end_date = models.DateField()
    end_date_timestamp = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50)
    client_selection = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_technology = models.JSONField(default=list)
    developer_name = models.JSONField(default=list)
    # ✅ Grouped as dictionaries now
    repo_links = models.JSONField(default=dict, blank=True)
    documents = models.JSONField(default=dict, blank=True)
    live_links = models.JSONField(default=dict, blank=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
