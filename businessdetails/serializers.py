from rest_framework import serializers
from .models import BusinessDetail, TeamSize

class BusinessDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = '__all__'
        read_only_fields = ['user']

class TeamSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSize
        fields = '__all__'
