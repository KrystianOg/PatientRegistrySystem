from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from ..models import User


class TestsSetup(APITestCase):
    def setUp(self):
        # define patient
        Group.objects.create(name='Patient')
        Group.objects.create(name='Doctor')
        self.patient_data = {
            'email': 'patient11@mail.com',
            'password': '12345678'
        }
        self.patient = User.objects.create_user(
            email=self.patient_data.get('email'),
            password=self.patient_data.get('password')
        )

        self.patient.is_active = True  # defaults to true
        self.patient.save()

        # define doctor
        self.doctor_data = {
            'email': 'doctor11@mail.com',
            'password': '12345678'
        }
        self.doctor = User.objects.create_user(
            email=self.doctor_data.get('email'),
            password=self.doctor_data.get('password')
        )
        self.doctor.is_active = True  # defaults to true
        self.doctor.save()
