from django.db import models
from django.conf import settings  # ✅ this is the fix

class BusinessDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_category = models.CharField(max_length=100)
    company_name = models.CharField(max_length=150)
    address = models.TextField()
    gstin = models.CharField(max_length=15)
    pan = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"
