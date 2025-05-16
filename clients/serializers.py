from rest_framework import serializers
from common_country_module.models import Country
from common_country_module.serializers import CountrySerializer
from accounts.serializers import ProfileSerializer  # import your user/profile serializer
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True,
        required=False
    )
    user = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['user']

    def get_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_staff:
            # ✅ Admin sees full profile
            return ProfileSerializer(obj.user, context=self.context).data
        # ✅ Normal user sees just the ID
        return obj.user.id if obj.user else None
