from rest_framework import serializers
from src.newstopics.models import NewsTopics
from src.news.models import News
from src.topics.models import Topics

class newsTopicsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    news = serializers.PrimaryKeyRelatedField(queryset=News.objects.all())
    topics = serializers.PrimaryKeyRelatedField(queryset=Topics.objects.all())
    is_delete = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """
        Create and return a new `News` instance, given the validated data.
        """
        return NewsTopics.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `News` instance, given the validated data.
        """
        instance.news = validated_data.get('news', instance.news)
        instance.topics = validated_data.get('topics', instance.topics)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        instance.save()
        return instance