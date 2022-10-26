from django.urls import reverse
from rest_framework import status

from api.apps.authentication.models import User
from api.apps.authentication.tests.setup import TestsSetup
from api.apps.core.models import Request


class TestCreateRequests(TestsSetup):
    def setUp(self):
        super().setUp()
        self.request_data = {
            "symptoms": ["headache", "stomachache"],
            "comment": "I have a headache and stomachache",
        }

    def test_patient_can_create_request_true(self):

        self.client.force_authenticate(user=self.patient)
        response = self.client.post(
            reverse("requests-list"),
            self.request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient"], self.patient.id)

    def test_doctor_can_create_request_true(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post(
            reverse("requests-list"),
            self.request_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient"], self.doctor.id)


class TestAccessRequest(TestsSetup):
    def setUp(self):
        super().setUp()
        self.other_user = User.objects.create_user(email="otheruser@mail.com", password="12345678")
        self.other_request = Request.objects.create(
            patient=self.other_user,
            symptoms=["headache", "stomachache"],
            comment="I have a headache and stomachache",
        )

    def test_patient_can_read_somebody_request_false(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.get(
            reverse("requests-detail", kwargs={"pk": self.other_request.id}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patient_can_read_self_request_true(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(
            reverse("requests-detail", kwargs={"pk": self.other_request.id}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_can_read_somebody_request_true(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.get(
            reverse("requests-detail", kwargs={"pk": self.other_request.id}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
