from rest_framework import serializers

from common_country_module.models import Country
from common_country_module.serializers import CountrySerializer
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True,
        required=False
    )
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['user']
