from rest_framework import serializers
from .models import Project
import time

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

class ProjectSerializer(serializers.ModelSerializer):
    live_links = LinkGroupSerializer(required=False)
    repo_links = LinkGroupSerializer(required=False)
    documents = DocumentGroupSerializer(required=False)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_developer_name(self, value):
        if not isinstance(value, list) or not all(isinstance(name, str) for name in value):
            raise serializers.ValidationError("developer_name must be a list of strings.")
        if not value:
            raise serializers.ValidationError("Developer list cannot be empty.")
        return value

    def validate_project_technology(self, value):
        if not isinstance(value, list) or not all(isinstance(tech, str) for tech in value):
            raise serializers.ValidationError("project_technology must be a list of strings.")
        return value

    def to_internal_value(self, data):
        """
        Override this method to ensure nested dicts (live_links, repo_links, documents) are converted properly.
        """
        live_links = data.get('live_links', {})
        repo_links = data.get('repo_links', {})
        documents = data.get('documents', {})

        if isinstance(live_links, dict):
            data['live_links'] = live_links
        if isinstance(repo_links, dict):
            data['repo_links'] = repo_links
        if isinstance(documents, dict):
            data['documents'] = documents

        return super().to_internal_value(data)

    def create(self, validated_data):
        live_links = validated_data.pop('live_links', {})
        repo_links = validated_data.pop('repo_links', {})
        documents = validated_data.pop('documents', {})

        validated_data['live_links'] = live_links
        validated_data['repo_links'] = repo_links
        validated_data['documents'] = documents

        # Timestamps
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')

        if start_date:
            validated_data['start_date_timestamp'] = int(time.mktime(start_date.timetuple()))
        if end_date:
            validated_data['end_date_timestamp'] = int(time.mktime(end_date.timetuple()))

        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Optional nested groups
        for field in ['live_links', 'repo_links', 'documents']:
            value = validated_data.pop(field, None)
            if value is not None:
                setattr(instance, field, value)

        # Optional list fields
        if 'developer_name' in validated_data:
            instance.developer_name = validated_data.pop('developer_name')
        if 'project_technology' in validated_data:
            instance.project_technology = validated_data.pop('project_technology')
        # Timestamps
        start_date = validated_data.get('start_date', instance.start_date)
        end_date = validated_data.get('end_date', instance.end_date)

        if start_date:
            instance.start_date_timestamp = int(time.mktime(start_date.timetuple()))
        if end_date:
            instance.end_date_timestamp = int(time.mktime(end_date.timetuple()))

        # Update remaining fields
        return super().update(instance, validated_data)
