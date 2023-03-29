from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from booking.models import (Enduser, User, Appointment, Availabledate)
from django.contrib.admin.widgets import AdminDateWidget



class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        return user


class EnduserSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_enduser = True
        user.save()
        enduser = Enduser.objects.create(user=user)
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['name', 'dose_type', 'vaccinetype', 'vaccinecenter','date_of_vaccine1', 'availabledate']
        widgets = {
            'date_of_vaccine1': DateInput(),
            # 'availabledate': DateInput(),
        }


class AvailabledateForm(forms.ModelForm):

    class Meta:
        model = Availabledate
        fields = ['name','date']
        # widgets = {
        #     'name': DateInput(),
        # }

