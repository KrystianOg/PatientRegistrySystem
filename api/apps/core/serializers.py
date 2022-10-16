from rest_framework import serializers
from .models import Appointment, Request, User


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
        read_only_fields = ['pk']

    def validate_doctor(self, value):
        if not value.type == User.UserType.DOCTOR:
            raise serializers.ValidationError(f'{value} is not a doctor.')
        return value


class AppointmentPatientSerializer(serializers.ModelSerializer):
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
        read_only_fields = [
            'pk',
            'doctor',
            'patient',
            'date',
            'duration',
            'patient_appeared',
            'comment'
        ]


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = [
            'pk',
            'patient',
            'symptoms',
            'comment'
        ]
        read_only_fields = ['pk']


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
        read_only_fields = ['pk']
