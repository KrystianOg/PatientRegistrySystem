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


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = [
            'pk',
            'patient',
            'symptoms',
            'comment'
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'pk',
            'type',
            'email',
            'first_name',
            'last_name'
        ]
