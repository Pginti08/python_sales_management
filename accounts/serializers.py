from rest_framework import serializers

from common_country_module.models import Country
from common_country_module.serializers import CountrySerializer
from .models import Category, SalesUser
from django.contrib.auth import authenticate, get_user_model

CustomUser = get_user_model()
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=True)

    class Meta:
        model = SalesUser
        fields = ['email', 'name', 'phone', 'country', 'password', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if SalesUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = SalesUser.objects.create_user(
            **validated_data
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password too short.",
        },
    )

    def validate(self, data):
        """Authenticate user using email instead of username."""
        email = data.get("email")
        password = data.get("password")

        # if email and password:
        user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

        if not user:
            raise serializers.ValidationError({'error': 'Unable to log in with provided credentials.'})

        data['user'] = user
        return data

class ProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = SalesUser
        fields = ['id', 'name', 'email', 'phone', 'country', 'address']
        read_only_fields = ['id', 'email', 'role']

