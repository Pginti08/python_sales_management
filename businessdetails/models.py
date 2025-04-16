from django.db import models
from django.conf import settings
from common_country_module.models import Country

class TeamSize(models.Model):
    size = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.size

class BusinessDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=150)
    team_size = models.ForeignKey(TeamSize, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.TextField()
    phone = models.CharField(max_length=25)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    gstin = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.business_name} ({self.user.name})"
