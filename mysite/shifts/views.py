from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
import calendar
from cleections import deque
import datetime
import .models import Schedule
from django.views.generic import ListView, FormView, DeleteView
from django.contrib import messages


class BaseCalendarMixin:
    """Base class for all calendar"""
    #0:starting on Monday, 1: starting on Tuesday, 6: starting on Sunday
    first_weekday = 0
    week_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def setup(self):
        """Setup calendar
        create instance for calender.Calendar class
        """
        self._calender = calender.Calender(self.first_weekday)

    def get_week_names(self):
        """changeable the first day for a week"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names

class WeekCalendarMixin(BaseCalendarMixin):
    """Base class for week calenar"""
    def get_week_days(self):
        #return all days in a week
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today().replace(day=1)
        #pickup the week
        for week in self.calendar.monthdatescalender(date.year, date.month):
            #if date is founded, return the week
            if date in week:
                return week

    def get_week_calendar(self):
        """retuns week calendar library"""
        self.setup()
        days = self.get_week_days()
        first = day[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'days': days,
            'previous':first - datetime.timedelta(days=7),
            'next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'first': first,
            'last': last,
        }
        return calendar_data

class WeekWithScheduleMixin(WeekCalendarMixin):
    """Edit shift in the week calendar"""
    model = Schedule
    date_field = 'date'
    order_field = 'start_time'

    def get_week_schedules(self, days):

        for day in days:
            lookup = {self.date_field: day}
            queryset = self.objects.filter(**lookup)
            if self.order_field:
                queryset = queryset.order_by(self.order_field)
            yield queryset


    def get_week_calendar(self):
        calendar_data = super().get_week_calendar()
        schedules = self.get_week_schedules(calendar_data['days'])
        calendar_data['schedule_list'] = schedules
        return calendar_data



class ShiftAddView(FormView):
    form = ScheduleForm()
    template_name = 'shifts/schedule_edit.html'
    success_url = reverse_lasy('shifts:index')

    def get(self,**kwargs):
        #kwargs=dictionary
        context = super().get(**kwargs)
        context['week'] = self.get_week_calendar()
        return context

    def post(self, request, *args, **kwargs):
        form = ScheduleForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, 'shifts.index.html', {'form':form})
        form.save(commit=True)
        messages.success(request, "'%s' has been just added" % form.cleaned_data[shifts])
        return redirect('shifts:index')

class ShiftDeleteView(DeleteView):
    model = Schedule
    success_url = reverse_lazy('shifts:index')

    def get(self, request, *args, **kwargs):
        return.post(request, *args, **kwargs)



@login_required
class Calendar(View):