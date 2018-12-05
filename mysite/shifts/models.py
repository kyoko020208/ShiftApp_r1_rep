from django.db import models
import datetime
from django.utils import timezone
from accouns.models import UserManager


class Manager(models.Model):
    manager = models.ForeignKey(UserManager, on_delete=models.CASCADE, related_name=Manager)


class Schedule(models.Model):
    start_time = models.TimeField('start time', default=datetime.time(7,0,0))
    end_time = models.TimeField('end time', default=datetime.time(7,0,0))
    date = models.DateField('date')
    created_at = models.DateField('date modified', default=datatime.time(7,0,0))

    def __str__(self):
        return self.date

# class TimeTable(models.Model):
#     start = models.TimeField(default='08:00')
#     end = models.TimeField(default='22:00')
#
#     def starftimetable(self):
#         timef = '%H:%M'
#         start,end = self.start,self.end
#         return "%s ~ %s" % ( start.st)