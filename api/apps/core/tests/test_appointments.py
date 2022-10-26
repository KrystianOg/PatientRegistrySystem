from django.urls import reverse
from rest_framework import status

from api.apps.authentication.models import User
from api.apps.authentication.tests.setup import TestsSetup
from api.apps.core.models import Request


class TestCreateAppointments(TestsSetup):
    def setUp(self):
        super().setUp()
        self.request = Request.objects.create(
            patient=self.patient,
            symptoms=["headache", "stomachache"],
            comment="I have a headache and stomachache",
        )
        self.appointment_data = {
            "request": self.request.id,
            "date": "2020-12-12T13:40",
            "duration": 30,
            "patient": self.patient.id,
        }

    def test_patient_can_create_appointment_false(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.post(
            reverse('appointments-list'),
            self.appointment_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doctor_can_create_appointment_true(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post(
            reverse('appointments-list'),
            self.appointment_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient'], self.patient.id)
        self.assertEqual(response.data['doctor'], self.doctor.id)


class TestAccessRequest(TestsSetup):
    def setUp(self):
        super().setUp()
        self.other_user = User.objects.create_user(
            email="otheruser@mail.com",
            password="12345678"
        )
        self.other_appointment = Request.objects.create(
            patient=self.other_user,
            symptoms=["headache", "stomachache"],
            comment="I have a headache and stomachache",
        )

    def test_patient_can_read_somebody_appointment_false(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.get(
            reverse('appointments-detail', kwargs={'pk': self.other_appointment.id}),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patient_can_read_self_appointment_true(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(
            reverse('appointments-detail', kwargs={'pk': self.other_appointment.id}),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_can_read_somebody_appointment_true(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.get(
            reverse('appointments-detail', kwargs={'pk': self.other_appointment.id}),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


