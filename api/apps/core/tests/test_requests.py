from django.urls import reverse
from rest_framework import status

from api.apps.authentication.models import User
from api.apps.authentication.tests.setup import TestsSetup


class TestRequests(TestsSetup):
    def test_patient_can_create_request(self):
        request_data = {
            "symptoms": ["headache", "stomachache"],
            "comment": "I have a headache and stomachache",
        }
        user = User.objects.get(email=self.patient_data.get("email"))
        self.client.force_authenticate(user=user)
        response = self.client.post(
            reverse('requests-list'),
            request_data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient'], self.patient.id)

