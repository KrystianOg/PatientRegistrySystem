from django.db.models import Q
from rest_framework import serializers
from .models import Appointment, Request, User


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["pk", "doctor", "patient", "date", "duration", "patient_appeared", "comment"]
        read_only_fields = ["pk"]

    def validate_doctor(self, doctor):
        if doctor.groups.filter(name="Doctor").exists():
            return doctor
        raise serializers.ValidationError("This user is not a doctor")

    def validate_patient(self, patient):
        if patient.groups.filter(name="Patient").exists():
            return patient
        raise serializers.ValidationError("This user is not a patient")

    # maybe can be simpler or has one queryset request only
    # need to be tested more
    def validate(self, attrs):
        if self.instance:
            pk = self.instance.pk

        duration = attrs.get("duration")
        appointment_start = attrs.get("date")
        appointment_stop = appointment_start + duration

        patient_appointments = Q(patient=attrs.get("patient"))
        doctor_appointments = Q(doctor=attrs.get("doctor"))
        users_appointments = patient_appointments | doctor_appointments

        starts_during_appointment = Q(date__gte=appointment_start) & Q(date__lte=appointment_stop)
        user_appointments_start_during_this_one = users_appointments & starts_during_appointment
        other_start_queryset = Appointment.objects.filter(user_appointments_start_during_this_one)
        if other_start_queryset.exists() and other_start_queryset.first().pk != pk:
            if other_start_queryset.first().doctor == attrs.get("doctor"):
                raise serializers.ValidationError("You start another appointment before it ends")
            raise serializers.ValidationError("Patient starts another appointment before it ends")

        appointments_before_appointment = users_appointments & Q(date__lte=appointment_start)

        earlier_appointment = (
            Appointment.objects.filter(appointments_before_appointment).order_by("date").last()
        )
        if (
            earlier_appointment
            and earlier_appointment.is_date_overlapping(appointment_start)
            and earlier_appointment.pk != pk
        ):
            if earlier_appointment.doctor == attrs.get("doctor"):
                raise serializers.ValidationError("Then you have another appointment in progress")
            raise serializers.ValidationError("Then patient have another appointment in progress")

        return attrs


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ["pk", "patient", "symptoms", "comment"]
        read_only_fields = ["pk"]

    def validate_patient(self, user):
        if user.groups.filter(name="Patient").exists():
            return user
        raise serializers.ValidationError("User is not a patient")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email", "first_name", "last_name"]
        read_only_fields = ["pk"]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        user_pk = request.user.pk
        user_to_be_changed_pk = request.data.get("pk")
        if user_pk != user_to_be_changed_pk:
            raise serializers.ValidationError("Trying to change different account")
        return super().update(instance, validated_data)
