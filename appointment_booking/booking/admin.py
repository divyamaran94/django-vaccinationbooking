from django.contrib import admin
from .models import User, Enduser, Vaccinetype, Vaccinecenter, Appointment, Availabledate

admin.site.register(User)
admin.site.register(Vaccinetype)
admin.site.register(Vaccinecenter)
admin.site.register(Availabledate)
admin.site.register(Appointment)
admin.site.register(Enduser)
