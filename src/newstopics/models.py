from django.db import models

from src.news.models import News
from src.topics.models import Topics

# Create your models here.
class NewsTopics(models.Model):
    class Meta:
        db_table = 'news_topics'

    news = models.ForeignKey(News, on_delete=models.CASCADE)
    topics = models.ForeignKey(Topics, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)