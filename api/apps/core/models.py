import datetime

from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver

from guardian.shortcuts import assign_perm

from api.apps.authentication.models import User


class Appointment(models.Model):
    """Model definition for Appointment."""

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_patient")
    date = models.DateTimeField()
    duration = models.DurationField()  # may change to integer if easier
    symptoms = ArrayField(models.CharField(max_length=64), size=None, blank=True, null=True)
    patient_appeared = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "appointments"
        ordering = ["-date"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(duration__gt=datetime.timedelta(minutes=1)),
                name="duration_is_positive",
            )
        ]

    @property
    def end_date(self):
        return self.date + self.duration

    def is_date_overlapping(self, date):
        return self.date <= date <= self.end_date

    def __str__(self):
        return f"{self.doctor} {self.patient} {self.date} {self.duration}"


@receiver(post_save, sender=Appointment)
def create_appointment_permissions(sender, instance=None, created=False, **kwargs):
    if created:
        # TODO: user notifications
        assign_perm("view_appointment", instance.doctor, instance)
        # patient should be notified when doctor changes appointment
        assign_perm("change_appointment", instance.doctor, instance)
        assign_perm("delete_appointment", instance.doctor, instance)
        # patient should be notified when doctor deletes appointment
        assign_perm("delete_appointment", instance.doctor, instance)

        assign_perm("view_appointment", instance.patient, instance)


class Request(models.Model):
    """Model definition for Request."""

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_patient")
    symptoms = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "requests"

    def __str__(self):
        return f"{self.patient} {self.symptoms}"


@receiver(post_save, sender=Request)
def create_requests_permissions(sender, instance=None, created=False, **kwargs):
    if created:
        # TODO: user notifications
        assign_perm("view_request", instance.patient, instance)
        assign_perm("change_request", instance.patient, instance)
        assign_perm("delete_request", instance.patient, instance)

        doctors_group = Group.objects.get(name="Doctor")
        # doctor
        assign_perm("view_request", doctors_group, instance)
        assign_perm("delete_request", doctors_group, instance)


# possible TODO: add a model for prescriptions if too few models
