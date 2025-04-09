from rest_framework import serializers
from .models import BusinessDetail

class BusinessDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = '__all__'  # include all fields
        read_only_fields = ['user']  # user will be set in view using request.user
