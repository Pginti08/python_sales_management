from django.db import models
from django.conf import settings
from common_country_module.models import Country

class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    city_town =  models.CharField(max_length=150)
    pan = models.TextField()
    phone = models.CharField(max_length=15)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    client_type = models.CharField(max_length=150)
    gstin = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.business_name
