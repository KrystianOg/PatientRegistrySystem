from django.db.models import Q
from rest_framework import serializers

from api.apps.authentication.serializers import UserSerializer
from api.apps.core.models import Appointment, Request


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id", "doctor", "patient", "date", "duration", "patient_appeared", "comment"]
        read_only_fields = ["id"]

    def validate_doctor(self, doctor):
        if doctor.groups.filter(name="Doctor").exists():
            return doctor
        raise serializers.ValidationError("This user is not a doctor")

    def validate_patient(self, patient):
        if patient.groups.filter(name="Patient").exists():
            return patient
        raise serializers.ValidationError("This user is not a patient")

    # only 2 db requests :) (80-100 ms)
    def validate(self, attrs):
        duration = attrs.get("duration")
        appointment_start = attrs.get("date")
        appointment_stop = appointment_start + duration

        patient_appointments = Q(patient=attrs.get("patient"))
        doctor_appointments = Q(doctor=attrs.get("doctor"))
        users_appointments = patient_appointments | doctor_appointments

        starts_during_appointment = Q(date__gte=appointment_start) & Q(date__lte=appointment_stop)
        user_appointments_start_during_this_one = users_appointments & starts_during_appointment
        other_start_queryset = Appointment.objects.filter(user_appointments_start_during_this_one)
        later_appointment = other_start_queryset.first()

        if later_appointment:
            if not self.instance or self.instance and not later_appointment.pk == self.instance.pk:
                if later_appointment.doctor == attrs.get("doctor"):
                    raise serializers.ValidationError(
                        "You start another appointment before it ends"
                    )
                raise serializers.ValidationError(
                    "Patient starts another appointment before it ends"
                )

        appointments_before_appointment = users_appointments & Q(date__lte=appointment_start)

        earlier_appointment = (
            Appointment.objects.filter(appointments_before_appointment).order_by("date").last()
        )
        if earlier_appointment:
            if (
                not self.instance
                or self.instance
                and not earlier_appointment.pk == self.instance.pk
            ):
                if earlier_appointment.is_date_overlapping(appointment_start):
                    if earlier_appointment.doctor == attrs.get("doctor"):
                        raise serializers.ValidationError(
                            "Then you have another appointment in progress"
                        )
                    raise serializers.ValidationError(
                        "Then patient have another appointment in progress"
                    )

        return attrs


class GetAppointmentSerializer(serializers.ModelSerializer):
    doctor = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "doctor", "patient", "date", "duration", "patient_appeared", "comment"]
        read_only_fields = ["id"]


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ["id", "patient", "symptoms", "comment"]
        read_only_fields = ["id"]

    def validate_patient(self, user):
        if user.groups.filter(name="Patient").exists():
            return user
        raise serializers.ValidationError("User is not a patient")


class GetRequestSerializer(RequestSerializer):
    patient = UserSerializer(read_only=True)
