from rest_framework import serializers
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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = SalesUser
        fields = ['username', 'email', 'name', 'phone', 'category', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
        min_length=5,
        max_length=10,
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