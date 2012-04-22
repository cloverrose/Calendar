from django.db import models

# Create your models here.
class Event(models.Model):
    day   = models.DateTimeField()
    event = models.CharField(max_length=256)
    url   = models.URLField()
