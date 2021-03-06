from django.db import models
import datetime
from django.utils import timezone

class Schedule(models.Model):
    class Meta:
        db_table = 'schedule'
    start_time = models.TimeField('start time', default=datetime.time(7,0,0))
    end_time = models.TimeField('end time', default=datetime.time(7,0,0))
    date = models.DateField('date', default=timezone.now)
    created_at = models.DateField('date modified', default=timezone.now)

    def __str__(self):
        return self.date

class Availability(models.Model):
    class Meta:
        db_table = 'availability'
    available = models.IntegerField()
    start_time = models.TimeField('start time', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('end time', default=datetime.time(7, 0, 0))
    created_at = models.DateField('date modified', default=timezone.now)

    def __str__(self):
        return self.available