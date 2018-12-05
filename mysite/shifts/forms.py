from django import forms

from shifts.models import Schedule
from accouns.models import UserManager

class ShiftAddForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('start_time', 'end_time', )

    def __init__(self, *args, **kwargs):
        super(ShiftAddForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs = {'placeholder' : 'Start time'}
        self.fields['start_time'].auto_focus = True
        self.fields['end_time'].widget.attrs = {'placeholder' : 'End Time'}
        self.fields['end_time'].auto_focus = True


    def save(self, commit=True):
        shift = super(ShiftAddForm, self).save(commit=False)
        get_shift_id = list(Schedule.objects.filter(shift=shift).values('pk'))
        shift.shift_id = get_shift_id[0]['pk']
        shif.iser = self.user
        if commit:
            shift.save()
        return shift