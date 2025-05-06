from rest_framework import serializers

from bankdetails.serializers import BankDetailSerializer
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
            'client',
            'business',
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

        # validate nested items explicitly
        items_serializer = InvoiceItemSerializer(data=items_data, many=True)
        items_serializer.is_valid(raise_exception=True)  # ✅ Will raise validation error if any

        invoice = Invoice.objects.create(**validated_data)

        # save nested items
        for item_data in items_serializer.validated_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')

        # validate nested items explicitly
        items_serializer = InvoiceItemSerializer(data=items_data, many=True)
        items_serializer.is_valid(raise_exception=True)  # ✅ Will raise validation error if any

        # update invoice fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # clear old items
        instance.items.all().delete()

        # save new items
        for item_data in items_serializer.validated_data:
            InvoiceItem.objects.create(invoice=instance, **item_data)

        return instance

class InvoiceListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    business = BusinessDetailSerializer(read_only=True)
    bank = BankDetailSerializer(read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
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
            'status',
            'items'
        ]