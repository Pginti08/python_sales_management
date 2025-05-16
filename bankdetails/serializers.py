from rest_framework import serializers
from .models import BankDetail
from accounts.serializers import ProfileSerializer  # Adjust import if needed

class BankDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = BankDetail
        fields = '__all__'
        read_only_fields = ['user']

    def get_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_staff:
            # ✅ Admin sees full profile
            return ProfileSerializer(obj.user, context=self.context).data
        # ✅ Normal user sees just the ID
        return obj.user.id if obj.user else None
