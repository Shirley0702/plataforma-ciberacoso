from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ParticipantFeedback


@override_settings(APP_VERSION="2.1.0-test")
class ParticipantFeedbackApiTests(APITestCase):
    endpoint = "/api/product-validation/feedback/"

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="participant",
            password="TestSegura2026!",
        )
        self.payload = {
            "ease_of_use": 4,
            "content_clarity": 5,
            "educational_usefulness": 5,
            "satisfaction": 4,
            "accessibility": 4,
            "open_comment": "La ruta fue clara y pude completarla con teclado.",
            "informed_consent": True,
        }

    def test_requires_authentication(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_participant_can_create_and_update_one_response_per_version(self):
        self.client.force_authenticate(self.user)

        created = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created.data["app_version"], "2.1.0-test")

        updated = self.client.post(
            self.endpoint,
            {**self.payload, "satisfaction": 5},
            format="json",
        )
        self.assertEqual(updated.status_code, status.HTTP_200_OK)
        self.assertEqual(ParticipantFeedback.objects.count(), 1)
        self.assertEqual(ParticipantFeedback.objects.get().satisfaction, 5)

        retrieved = self.client.get(self.endpoint)
        self.assertEqual(retrieved.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieved.data["satisfaction"], 5)

    def test_rejects_out_of_range_scores_and_missing_consent(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.endpoint,
            {**self.payload, "ease_of_use": 6, "informed_consent": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ease_of_use", response.data)
        self.assertIn("informed_consent", response.data)

    def test_administrator_cannot_submit_participant_feedback(self):
        admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="AdminSegura2026!",
        )
        self.client.force_authenticate(admin)
        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
