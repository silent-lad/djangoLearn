from django.contrib import admin
from .models import Hospital, Appointment, Profile

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Appointment)
admin.site.register(Profile)
