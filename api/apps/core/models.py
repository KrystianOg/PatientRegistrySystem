from django.db import models

from django.contrib.postgres.fields import ArrayField

from api.apps.authentication.models import User


class Appointment(models.Model):
    """Model definition for Appointment."""

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_patient")
    # TODO: add custom validator
    #  [ ] so doctor can not have two appointments at the same time
    #  [ ] so patient can not have two appointments at the same time
    date = models.DateTimeField()
    duration = models.DurationField()  # may change to integer if easier
    patient_appeared = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "appointments"
        ordering = ["-date"]


class Request(models.Model):
    """Model definition for Request."""

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_patient")
    symptoms = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "requests"


# possible TODO: add a model for prescriptions if too few models
