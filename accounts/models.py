from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # ⚠️ No validation of name/phone/category here — superuser can skip
        return self.create_user(email, username, password, **extra_fields)


class SalesUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)  # allow blank/null
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # for createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email
