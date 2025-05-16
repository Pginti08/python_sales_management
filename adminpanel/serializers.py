
from rest_framework import serializers
from accounts.models import SalesUser


# accounts/serializers.py
 # assuming SalesUser is your user model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesUser
        fields = '__all__'  # or specify required fields
