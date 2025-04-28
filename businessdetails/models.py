from django.db import models
from django.conf import settings
from common_country_module.models import Country

class TeamSize(models.Model):
    size = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.size

class BusinessDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, default='unknown')
    business_name = models.CharField(max_length=150)
    team_size = models.ForeignKey(TeamSize, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.TextField()
    phone = models.CharField(max_length=25)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    street_address = models.TextField()
    postal_code = models.CharField(max_length=15, default='unknown')
    gstin = models.CharField(max_length=25)
    tax = models.CharField(max_length=15, null=True, blank=True)
    logo = models.ImageField(upload_to='business/logos/', null=True, blank=True)  # Optional field

    def __str__(self):
        return f"{self.business_name} ({self.user.name})"
