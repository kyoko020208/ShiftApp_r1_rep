from django import forms
from shifts.models import Schedule, Availability
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


class AvailabilityAddForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ('start_time', 'end_time', 'available', )
        CHOICE = {
            ('0', 'OK'),
            ('1', 'NG'),
        }
        available_info = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICE)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AvailabilityAddForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs = {'placeholder': 'Start time'}
        self.field['start_time'].auto_focus = True
        self.fields['end_time'].widget.attrs = {'placeholder': 'End Time'}
        self.fields['end_time'].auto_focus = True
        self.fields['available'] = self.get.available_info

    def clean(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_data']
        choices = self.cleaned_data['choice_field']
        available = self.cleaned_data['available_info']

        if choices == 1 and start_time != None:
            raise forms.ValidationError("choose OK")
        if choices == 1 and end_time != None:
            raise forms.ValidationError("choose OK")
        
    def save(self, commit=True):
        availability_info = super(AvailabilityAddForm, self).save(commit=False)
        if commit:
            availability_info.save()
            # UserManager.objects.create(user=user_info)

        return availability_info
