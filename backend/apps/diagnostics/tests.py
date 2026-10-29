from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.courses.models import CourseUnit

from .models import DiagnosticOption, DiagnosticQuestion, DiagnosticResult
from .ml.model import load_model


class DiagnosticTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "demo", password="TestSegura2026!"
        )
        self.client.force_authenticate(self.user)
        self.vertical = CourseUnit.objects.create(
            title="Acoso Vertical", slug="acoso-vertical", description="Vertical", order=1
        )
        self.technology = CourseUnit.objects.create(
            title="Acoso Tecnológico",
            slug="acoso-tecnologico",
            description="Tecnológico",
            order=3,
        )
        self.question_one = DiagnosticQuestion.objects.create(
            text="Escenario uno", primary_unit=self.vertical, order=1
        )
        self.question_two = DiagnosticQuestion.objects.create(
            text="Escenario dos", primary_unit=self.technology, order=2
        )
        self.vertical_option = DiagnosticOption.objects.create(
            question=self.question_one,
            label="Situación vertical",
            destination_unit=self.vertical,
            weight=10,
            order=1,
        )
        self.technology_option = DiagnosticOption.objects.create(
            question=self.question_two,
            label="Situación tecnológica",
            destination_unit=self.technology,
            weight=5,
            order=1,
        )
        self.neutral_one = DiagnosticOption.objects.create(
            question=self.question_one, label="Situación respetuosa", weight=0, order=2
        )
        self.neutral_two = DiagnosticOption.objects.create(
            question=self.question_two, label="Situación respetuosa", weight=0, order=2
        )

    def submit(self, first_option, second_option):
        return self.client.post(
            "/api/diagnostics/submit/",
            {
                "answers": [
                    {"question_id": self.question_one.id, "option_id": first_option.id},
                    {"question_id": self.question_two.id, "option_id": second_option.id},
                ]
            },
            format="json",
        )

    def test_submit_uses_machine_learning_for_a_clear_pattern(self):
        response = self.submit(self.vertical_option, self.technology_option)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["suggested_unit"]["id"], self.vertical.id)
        self.assertEqual(response.data["maximum_score"], 10)
        self.assertEqual(len(response.data["module_scores"]), 2)
        result = DiagnosticResult.objects.latest("id")
        self.assertEqual(
            result.recommendation_method,
            DiagnosticResult.RecommendationMethod.MACHINE_LEARNING,
        )
        self.assertEqual(result.model_version, "route-logistic-regression-v1")
        self.assertGreater(result.model_confidence, 0)
        self.assertLessEqual(result.model_confidence, 1)

    def test_submit_uses_preventive_technology_route_for_neutral_answers(self):
        response = self.submit(self.neutral_one, self.neutral_two)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["suggested_unit"]["id"], self.technology.id)
        self.assertEqual(response.data["maximum_score"], 0)
        result = DiagnosticResult.objects.latest("id")
        self.assertEqual(
            result.recommendation_method,
            DiagnosticResult.RecommendationMethod.RULE_FALLBACK,
        )
        self.assertIsNone(result.model_confidence)

    def test_submit_requires_every_active_scenario(self):
        response = self.client.post(
            "/api/diagnostics/submit/",
            {
                "answers": [
                    {
                        "question_id": self.question_one.id,
                        "option_id": self.vertical_option.id,
                    }
                ]
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_question_api_does_not_reveal_module_or_weights(self):
        response = self.client.get("/api/diagnostics/questions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("module_title", response.data[0])
        self.assertNotIn("weight", response.data[0]["options"][0])
        self.assertNotIn("destination_unit", response.data[0]["options"][0])

    def test_model_is_trained_and_keeps_validation_metadata(self):
        artifact = load_model()
        self.assertEqual(artifact["version"], "route-logistic-regression-v1")
        self.assertEqual(artifact["training_source"], "expert_bootstrap_synthetic")
        self.assertGreaterEqual(artifact["validation_accuracy"], 0.85)
