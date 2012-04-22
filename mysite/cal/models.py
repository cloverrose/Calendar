from django.db import models

# Create your models here.
class Event(models.Model):
    day   = models.DateTimeField()
    event = models.CharField(max_length=256)
    url   = models.URLField()

class User(models.Model):
    name  = models.CharField(max_length=200)
    events= models.ManyToManyField(Event)
