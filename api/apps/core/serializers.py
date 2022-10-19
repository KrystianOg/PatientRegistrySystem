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

    def validate_date(self, attrs):
        pass


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
        if not user_pk == user_to_be_changed_pk:
            raise serializers.ValidationError("Trying to change different account")
        return super().update(instance, validated_data)
