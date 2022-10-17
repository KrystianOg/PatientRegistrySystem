from django.contrib import admin
from .models import Appointment, Request
from guardian.admin import GuardedModelAdmin


@admin.register(Appointment)
class AppointmentAdmin(GuardedModelAdmin):
    pass


@admin.register(Request)
class RequestAdmin(GuardedModelAdmin):
    pass
