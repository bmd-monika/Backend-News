from django.db import models
# Create your models here.
class News(models.Model):
    news = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    is_delete = models.BooleanField(default=False)