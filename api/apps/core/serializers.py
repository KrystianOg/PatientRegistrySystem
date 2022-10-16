from rest_framework import serializers
from .models import Appointment, Request, User
from rest_framework.exceptions import PermissionDenied


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            'pk',
            'doctor',
            'patient',
            'date',
            'duration',
            'patient_appeared',
            'comment'
        ]


    def validate_doctor(self, value):
        if not value.type == User.UserType.DOCTOR:
            raise serializers.ValidationError(f'{value} is not a doctor.')
        return value

    def validate_patient(self, value):
        if not value.type == User.UserType.PATIENT:
            raise serializers.ValidationError(f'{value} is not a patient.')
        return value


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = [
            'pk',
            'patient',
            'symptoms',
            'comment'
        ]

    def validate_patient(self, value):
        if not value.type == User.UserType.PATIENT:
            raise PermissionDenied(f'{value} is not a patient.')
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'pk',
            'type',
            'type_detail',
            'email',
            'first_name',
            'last_name'
        ]
