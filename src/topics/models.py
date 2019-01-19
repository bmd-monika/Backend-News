from django.db import models
# Create your models here.
class Topics(models.Model):
    topics = models.CharField(max_length=50, null=True, blank=True)
    is_delete = models.BooleanField(default=False)