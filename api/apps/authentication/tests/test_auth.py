from django.urls import reverse
from rest_framework import status
from .setup import TestsSetup


class TestAuthentication(TestsSetup):
    def test_can_patient_login(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            self.patient_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

        self.patient_access = response.data['access']

    def test_can_doctor_login(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            self.doctor_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

        self.doctor_access = response.data['access']
