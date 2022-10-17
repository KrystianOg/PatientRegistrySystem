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
        fields = ["pk", "type", "type_detail", "email", "first_name", "last_name"]
        read_only_fields = ["pk"]

    # TODO: patients and doctors should be able to change ONLY their accounts
