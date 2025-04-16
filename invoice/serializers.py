from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['name', 'quantity', 'price', 'igst', 'gst']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=True, allow_empty=False) # Define nested serializer for items

    class Meta:
        model = Invoice
        fields = [ 'invoice_number', 'invoice_date', 'country', 'due_date', 'client', 'bank', 'business', 'items']

        read_only_fields = ['user']  # Ensure the user is automatically set

    def create(self, validated_data):
        # Extract the `items` data from validated_data
        items_data = validated_data.pop('items')

        # Create the Invoice object
        invoice = Invoice.objects.create(**validated_data)

        # Create the associated InvoiceItems
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        return invoice
