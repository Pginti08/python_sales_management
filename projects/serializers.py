from rest_framework import serializers
from .models import Project
from clients.models import Client
from common_country_module.models import Country
import time


# Developer info schema
class DeveloperSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


# Optional links
class LinkGroupSerializer(serializers.Serializer):
    website = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    iosApp = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    android = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    adminPanel = serializers.URLField(required=False, allow_blank=True, allow_null=True)


# Optional documents
class DocumentGroupSerializer(serializers.Serializer):
    link1 = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    link2 = serializers.CharField(required=False, allow_blank=True, allow_null=True)


# Project main serializer
class ProjectSerializer(serializers.ModelSerializer):
    developer_name = DeveloperSerializer(many=True, required=True)
    live_links = LinkGroupSerializer(required=False)
    repo_links = LinkGroupSerializer(required=False)
    documents = DocumentGroupSerializer(required=False)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_developer_name(self, value):
        if not value:
            raise serializers.ValidationError("Developer list cannot be empty.")
        return value

    def validate_project_technology(self, value):
        if not isinstance(value, list) or not all(isinstance(tech, str) for tech in value):
            raise serializers.ValidationError("project_technology must be a list of strings.")
        return value

    def to_representation(self, instance):
        """Customize the response format"""
        representation = super().to_representation(instance)

        # Convert date fields to strings
        representation['start_date'] = instance.start_date.strftime('%Y-%m-%d')
        representation['end_date'] = instance.end_date.strftime('%Y-%m-%d')

        # Ensure the developer_name field is a list of dicts with id and name
        representation['developer_name'] = [{'id': dev['id'], 'name': dev['name']} for dev in instance.developer_name]

        return representation

    def create(self, validated_data):
        developer_data = validated_data.pop('developer_name')
        live_links = validated_data.pop('live_links', {})
        repo_links = validated_data.pop('repo_links', {})
        documents = validated_data.pop('documents', {})

        # Convert nested serializer data to raw dicts
        validated_data['developer_name'] = developer_data
        validated_data['live_links'] = live_links
        validated_data['repo_link'] = repo_links
        validated_data['documents'] = documents

        # Add timestamps
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')

        if start_date:
            validated_data['start_date_timestamp'] = int(time.mktime(start_date.timetuple()))
        if end_date:
            validated_data['end_date_timestamp'] = int(time.mktime(end_date.timetuple()))

        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        developer_data = validated_data.pop('developer_name', None)
        live_links = validated_data.pop('live_links', None)
        repo_links = validated_data.pop('repo_link', None)
        documents = validated_data.pop('documents', None)

        if developer_data is not None:
            instance.developer_name = developer_data
        if live_links is not None:
            instance.live_links = live_links
        if repo_links is not None:
            instance.repo_link = repo_links
        if documents is not None:
            instance.documents = documents

        start_date = validated_data.get('start_date', instance.start_date)
        end_date = validated_data.get('end_date', instance.end_date)

        if start_date:
            validated_data['start_date_timestamp'] = int(time.mktime(start_date.timetuple()))
        if end_date:
            validated_data['end_date_timestamp'] = int(time.mktime(end_date.timetuple()))

        return super().update(instance, validated_data)
