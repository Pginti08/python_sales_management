from django.db import models

from clients.models import Client
from common_country_module.models import Country
from salesmanagement import settings


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
    project_technology = models.CharField(max_length=255)
    repo_link = models.URLField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    developer_name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    iosApp = models.URLField(blank=True, null=True)
    android = models.URLField(blank=True, null=True)
    adminPanel = models.URLField(blank=True, null=True)
    document1 = models.URLField(blank=True, null=True)
    document2 = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name
