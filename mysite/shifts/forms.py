from django import forms

from shifts.models import Schedule
from django.utils import timezone
from accounts.models import UserManager

class ShiftAddForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('start_time', 'end_time', 'date', )

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ShiftAddForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs = {'placeholder': 'Start time'}
        self.fields['start_time'].auto_focus = True
        self.fields['end_time'].widget.attrs = {'placeholder': 'End Time'}
        self.fields['end_time'].auto_focus = True
        self.fields['date'].widget.attrs = {'placeholder': 'timezone.now'}

    def save(self, commit=True):
        shift_info = super(ShiftAddForm, self).save(commit=False)
        shift_info.user = self._user
        if commit:
            shift_info.save()
        return shift_info