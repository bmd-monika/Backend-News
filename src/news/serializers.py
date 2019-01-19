from rest_framework import serializers
from src.news.models import News

class newsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    news = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    is_delete = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """
        Create and return a new `News` instance, given the validated data.
        """
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `News` instance, given the validated data.
        """
        instance.news = validated_data.get('news', instance.news)
        instance.status = validated_data.get('status', instance.status)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        instance.save()
        return instance