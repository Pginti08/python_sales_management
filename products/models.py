from django.db import models
from django.conf import settings
from common_country_module.models import Country

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    country_of_supply = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.amount
