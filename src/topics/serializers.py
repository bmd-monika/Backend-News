from rest_framework import serializers
from src.topics.models import Topics

class topicsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topics = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    is_delete = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """
        Create and return a new `Topics` instance, given the validated data.
        """
        return Topics.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Topics` instance, given the validated data.
        """
        instance.topics = validated_data.get('topics', instance.topics)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        instance.save()
        return instance