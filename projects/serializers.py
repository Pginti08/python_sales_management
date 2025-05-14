# from rest_framework import serializers
# from .models import Project
# import time
#
# class ProjectSerializer(serializers.ModelSerializer):
#     repo_link = serializers.ListField(
#         child=serializers.URLField(),
#         required=True
#     )
#     developer_name = serializers.ListField(
#         child=serializers.CharField(),
#         required=True
#     )
#
#     # Optional fields (no validation on items)
#     website = serializers.ListField(
#         child=serializers.URLField(),
#         required=False,
#         allow_null=True
#     )
#     iosApp = serializers.ListField(
#         child=serializers.URLField(),
#         required=False,
#         allow_null=True
#     )
#     android = serializers.ListField(
#         child=serializers.URLField(),
#         required=False,
#         allow_null=True
#     )
#     adminPanel = serializers.ListField(
#         child=serializers.URLField(),
#         required=False,
#         allow_null=True
#     )
#     document1 = serializers.ListField(
#         child=serializers.CharField(),
#         required=False,
#         allow_null=True
#     )
#     document2 = serializers.ListField(
#         child=serializers.CharField(),
#         required=False,
#         allow_null=True
#     )
#     class Meta:
#         model = Project
#         fields = '__all__'
#         read_only_fields = ['user', 'created_at', 'updated_at']
#
#     def create(self, validated_data):
#         # Calculate timestamps
#         start_date = validated_data.get('start_date')
#         end_date = validated_data.get('end_date')
#
#         if start_date:
#             validated_data['start_date_timestamp'] = int(time.mktime(start_date.timetuple()))
#         if end_date:
#             validated_data['end_date_timestamp'] = int(time.mktime(end_date.timetuple()))
#
#         # Set user automatically
#         validated_data['user'] = self.context['request'].user
#
#         return super().create(validated_data)
#
#     def update(self, instance, validated_data):
#         start_date = validated_data.get('start_date', instance.start_date)
#         end_date = validated_data.get('end_date', instance.end_date)
#
#         if start_date:
#             validated_data['start_date_timestamp'] = int(time.mktime(start_date.timetuple()))
#         if end_date:
#             validated_data['end_date_timestamp'] = int(time.mktime(end_date.timetuple()))
#
#         return super().update(instance, validated_data)
