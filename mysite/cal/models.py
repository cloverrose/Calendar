from django.db import models

# Create your models here.
class Event(models.Model):
    day   = models.DateTimeField()
    event = models.CharField(max_length=256)
    url   = models.URLField()

class User(models.Model):
    name  = models.CharField(max_length=200)
    events= models.ManyToManyField(Event)
    WEEKDAY_CHOICE = (
          ('Mon','Monday')
         ,('Tue','Tuesday')
         ,('Wed','Wednesday')
         ,('Thu','Thursday')
         ,('Fri','Friday')
         ,('Sat','Saturday')
         ,('Sun','Sunday')
        )
    start_weekday = models.CharField(max_length=3,choices=WEEKDAY_CHOICE,default='Mon')
