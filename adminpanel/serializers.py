from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from bankdetails.models import BankDetail
from businessdetails.models import BusinessDetail
from common_country_module.models import Country
from invoice.models import Invoice, InvoiceItem
from clients.models import Client
from projects.models import Project
from rest_framework import serializers
from accounts.models import SalesUser

class BankDetailSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    class Meta:
        model = BankDetail
        fields = '__all__'

class countrySerializer(serializers.ModelSerializer):
       class Meta:
        model = Country
        fields = '__all__'


class BusinessDetailSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    class Meta:
        model = BusinessDetail
        fields = '__all__'



class ClientSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
# accounts/serializers.py
 # assuming SalesUser is your user model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesUser
        fields = '__all__'  # or specify required fields
