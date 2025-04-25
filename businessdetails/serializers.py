from rest_framework import serializers

from common_country_module.models import Country
from .models import BusinessDetail, TeamSize
from common_country_module.serializers import CountrySerializer

class TeamSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSize
        fields = '__all__'

class BusinessDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    team_size = TeamSizeSerializer(read_only=True)

    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True
    )
    team_size_id = serializers.PrimaryKeyRelatedField(
        queryset=TeamSize.objects.all(),
        source='team_size',
        write_only=True
    )

    class Meta:
        model = BusinessDetail
        fields = '__all__'
        read_only_fields = ['user']