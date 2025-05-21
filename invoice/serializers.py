from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from bankdetails.models import BankDetail
from bankdetails.serializers import BankDetailSerializer
from businessdetails.models import BusinessDetail
from businessdetails.serializers import BusinessDetailSerializer

from clients.models import Client
from clients.serializers import ClientSerializer

from common_country_module.models import Country
from common_country_module.serializers import CountrySerializer

from .models import Invoice, InvoiceItem
from rest_framework.fields import FileField
from rest_framework.exceptions import ValidationError

class SafeFileField(FileField):
    def to_internal_value(self, data):
        if data in ['', None, 'null']:
            return 'unknown'  # allow empty input without throwing error

        try:
            return super().to_internal_value(data)
        except ValidationError:
            raise ValidationError("Please upload a valid file.")

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['name', 'quantity', 'price', 'igst', 'gst']


class InvoiceSerializer(serializers.ModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(
        queryset=BankDetail.objects.all(),
        required=False,
        allow_null=True
    )
    items = InvoiceItemSerializer(many=True, required=True)
    invoice_logo = SafeFileField(required=False, allow_null=True)
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
    user = serializers.SerializerMethodField()
    country = CountrySerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    business = BusinessDetailSerializer(read_only=True)
    bank = BankDetailSerializer(read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
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
            'invoice_logo',
            'status',
            'items'
        ]
    def get_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_staff:
            # ✅ Admin sees full profile
            return ProfileSerializer(obj.user, context=self.context).data
        # ✅ Normal user sees just the ID
        return obj.user.id if obj.user else None