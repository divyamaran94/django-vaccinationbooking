from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from datetime import date
from django.utils.translation import gettext as _


class User(AbstractUser):
    is_enduser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


class Vaccinetype(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vaccinetypes')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Vaccinecenter(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vaccinecenters')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Availabledate(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabledates')
    name = models.CharField(max_length=255)
    date = models.DateField()


    def __str__(self):
        return str(self.date)

class Appointment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=255)
    DOSE_CHOICES = [
        ("First Dose", "First Dose"),
        ("Second Dose", "Second Dose"),
        ("Booster Dose", "Booster Dose"),
    ]
    dose_type = models.CharField(
        max_length=255,
        choices=DOSE_CHOICES,
        default="First Dose",
    )
    vaccinetype = models.ForeignKey(Vaccinetype, on_delete=models.CASCADE, related_name='appointments')
    vaccinecenter = models.ForeignKey(Vaccinecenter, on_delete=models.CASCADE, related_name='vaccinecenters')
    availabledate = models.ForeignKey(Availabledate, on_delete=models.CASCADE, related_name='availabledates')
    date_of_vaccine1 = models.DateField()

    
    def __str__(self):
        return self.name

class Enduser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username
