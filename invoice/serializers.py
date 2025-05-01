from rest_framework import serializers

from businessdetails.models import BusinessDetail
from businessdetails.serializers import BusinessDetailSerializer

from clients.models import Client
from clients.serializers import ClientSerializer

from common_country_module.models import Country
from common_country_module.serializers import CountrySerializer

from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['name', 'quantity', 'price', 'igst', 'gst']


class InvoiceSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    business = BusinessDetailSerializer(read_only=True)

    country_id = serializers.IntegerField(write_only=True, required=True)
    client_id = serializers.IntegerField(write_only=True, required=True)
    business_id = serializers.IntegerField(write_only=True, required=True)

    items = InvoiceItemSerializer(many=True, required=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'user',
            'invoice_number',
            'invoice_date',
            'due_date',
            'bank',
            'country',
            'country_id',
            'client',
            'client_id',
            'business',
            'business_id',
            'status',
            'items',
            'invoice_logo',
        ]
        read_only_fields = ['user', 'id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        view = self.context.get('view')
        if request and view and getattr(view, 'action', None) == 'list':
            self.fields.pop('items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        country_id = validated_data.pop('country_id')
        client_id = validated_data.pop('client_id')
        business_id = validated_data.pop('business_id')

        invoice = Invoice.objects.create(
            **validated_data,
            country_id=country_id,
            client_id=client_id,
            business_id=business_id
        )

        for item in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')

        country_id = validated_data.pop('country_id', None)
        client_id = validated_data.pop('client_id', None)
        business_id = validated_data.pop('business_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if country_id is not None:
            instance.country_id = country_id
        if client_id is not None:
            instance.client_id = client_id
        if business_id is not None:
            instance.business_id = business_id

        instance.save()

        instance.items.all().delete()
        for item in items_data:
            InvoiceItem.objects.create(invoice=instance, **item)

        return instance

class InvoiceListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    business = BusinessDetailSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'invoice_date',
            'due_date',
            'bank',
            'country',
            'client',
            'business',
            'invoice_logo',
        ]