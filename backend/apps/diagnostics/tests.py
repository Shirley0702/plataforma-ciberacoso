from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.courses.models import CourseUnit

from .models import DiagnosticOption, DiagnosticQuestion, DiagnosticResult


class DiagnosticTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "demo", password="TestSegura2026!"
        )
        self.client.force_authenticate(self.user)
        self.units = [
            CourseUnit.objects.create(
                title="Relaciones de autoridad",
                slug="acoso-vertical",
                description="Autoridad",
                order=1,
            ),
            CourseUnit.objects.create(
                title="Relaciones entre pares",
                slug="acoso-horizontal",
                description="Pares",
                order=2,
            ),
            CourseUnit.objects.create(
                title="Seguridad digital",
                slug="acoso-tecnologico",
                description="Digital",
                order=3,
            ),
            CourseUnit.objects.create(
                title="Diversidad",
                slug="acoso-vulnerabilidad",
                description="Diversidad",
                order=4,
            ),
        ]
        self.preventive = CourseUnit.objects.create(
            title="Ruta preventiva",
            slug="fundamentos-preventivos",
            description="Prevención",
            order=5,
        )
        weights = (3, 2, 2, 1)
        self.questions = []
        self.weighted_options = []
        self.neutral_options = []
        for order, (unit, weight) in enumerate(zip(self.units, weights), start=1):
            question = DiagnosticQuestion.objects.create(
                text=f"Escenario {order}", primary_unit=unit, order=order
            )
            self.questions.append(question)
            self.weighted_options.append(
                DiagnosticOption.objects.create(
                    question=question,
                    label="Patrón observado",
                    destination_unit=unit,
                    weight=weight,
                    order=1,
                )
            )
            self.neutral_options.append(
                DiagnosticOption.objects.create(
                    question=question,
                    label="Dinámica respetuosa",
                    destination_unit=unit,
                    weight=0,
                    order=2,
                )
            )

    def submit(self, options):
        return self.client.post(
            "/api/diagnostics/submit/",
            {
                "answers": [
                    {"question_id": question.id, "option_id": option.id}
                    for question, option in zip(self.questions, options)
                ]
            },
            format="json",
        )

    def test_submit_builds_profile_and_preserves_ties_in_top_two_bands(self):
        response = self.submit(self.weighted_options)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["suggested_unit"]["id"], self.units[0].id)
        self.assertEqual(
            [unit["id"] for unit in response.data["recommended_units"]],
            [self.units[0].id, self.units[1].id, self.units[2].id],
        )
        self.assertEqual(response.data["route_type"], "prioritized")
        self.assertEqual(len(response.data["dimension_profile"]), 4)
        priorities = {
            dimension["unit_id"]: dimension["priority"]
            for dimension in response.data["dimension_profile"]
        }
        self.assertEqual(priorities[self.units[0].id], 1)
        self.assertEqual(priorities[self.units[1].id], 2)
        self.assertEqual(priorities[self.units[2].id], 2)
        result = DiagnosticResult.objects.latest("id")
        self.assertEqual(result.scoring_version, "multidimensional-profile-v2")
        self.assertEqual(
            result.profile["recommended_unit_ids"],
            [self.units[0].id, self.units[1].id, self.units[2].id],
        )

    def test_submit_uses_general_preventive_route_for_neutral_answers(self):
        response = self.submit(self.neutral_options)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["suggested_unit"]["id"], self.preventive.id)
        self.assertEqual(response.data["maximum_score"], 0)
        self.assertEqual(response.data["route_type"], "preventive_general")
        self.assertEqual(
            [unit["id"] for unit in response.data["recommended_units"]],
            [self.preventive.id],
        )

    def test_submit_requires_every_active_scenario(self):
        response = self.client.post(
            "/api/diagnostics/submit/",
            {
                "answers": [
                    {
                        "question_id": self.questions[0].id,
                        "option_id": self.weighted_options[0].id,
                    }
                ]
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_question_api_does_not_reveal_dimensions_or_weights(self):
        response = self.client.get("/api/diagnostics/questions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("primary_unit", response.data[0])
        self.assertNotIn("weight", response.data[0]["options"][0])
        self.assertNotIn("destination_unit", response.data[0]["options"][0])
