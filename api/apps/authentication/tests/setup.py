from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase
from ..models import User


class TestsSetup(APITestCase):
    def setUp(self):
        # define patient
        self.create_patient_group()
        self.create_doctor_group()

        self.patient_data = {"email": "patient11@mail.com", "password": "12345678"}
        self.patient = User.objects.create_user(
            email=self.patient_data.get("email"), password=self.patient_data.get("password")
        )

        self.patient.is_active = True  # defaults to true
        self.patient.save()

        # define doctor
        self.doctor_data = {"email": "doctor11@mail.com", "password": "12345678"}
        self.doctor = User.objects.create_doctor(
            email=self.doctor_data.get("email"), password=self.doctor_data.get("password")
        )
        self.doctor.is_active = True  # defaults to true
        self.doctor.save()

    def create_patient_group(self):
        group = Group.objects.create(name="Patient")
        permissions = Permission.objects.filter(
            codename__in=[
                "view_appointment",
                "add_request",
                "change_request",
                "delete_request",
                "view_request",
            ]
        )
        group.permissions.set(permissions)

    def create_doctor_group(self):
        group = Group.objects.create(name="Doctor")
        permissions = Permission.objects.filter(
            codename__in=[
                "add_request",
                "change_request",
                "delete_request",
                "view_request",
                "add_appointment",
                "change_appointment",
                "delete_appointment",
                "view_appointment",
            ]
        )
        group.permissions.add(*permissions)
