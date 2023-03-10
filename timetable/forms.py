from django.forms import ModelForm
from django import forms
from datetime import datetime, timedelta,date
from .models import Slot
from django.core.exceptions import ValidationError


class TimeSlotModelForm(ModelForm):
    class Meta:
        model = Slot
        fields = ['timeslot','endslot','day', 'year','week','user']


    def clean(self):
        data = self.cleaned_data
        duration = datetime.combine(date.min, data.get('endslot')) - datetime.combine(date.min, data.get('timeslot'))
        if Slot.objects.filter(timeslot__gte=data.get('timeslot'),user=data.get('user')):
                raise ValidationError(" You have already regesterd this slot")

        elif duration > timedelta(seconds=900):
            raise ValidationError("The duration can not be greater than 15 mins")
        elif duration < timedelta(seconds=900):
            raise ValidationError("The duration can not be less than 15 mins")