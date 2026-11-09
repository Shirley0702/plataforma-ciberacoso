from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.diagnostics.models import DiagnosticAttempt, DiagnosticResult

from .models import Certificate, CourseUnit, Lesson, ModuleQuizOption, ModuleQuizQuestion


class CourseProgressTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "demo", password="TestSegura2026!"
        )
        self.client.force_authenticate(self.user)
        self.assigned_unit = CourseUnit.objects.create(
            title="Ruta asignada", slug="ruta-asignada", description="Asignada", order=1
        )
        self.other_unit = CourseUnit.objects.create(
            title="Otra ruta", slug="otra-ruta", description="Otra", order=2
        )
        self.unassigned_unit = CourseUnit.objects.create(
            title="Ruta no asignada",
            slug="ruta-no-asignada",
            description="No asignada",
            order=3,
        )
        self.lesson = Lesson.objects.create(
            unit=self.assigned_unit, title="Lección", summary="Resumen", content="Contenido"
        )
        self.other_lesson = Lesson.objects.create(
            unit=self.other_unit,
            title="Segunda lección asignada",
            summary="Resumen",
            content="Contenido",
        )
        self.unassigned_lesson = Lesson.objects.create(
            unit=self.unassigned_unit,
            title="Lección ajena",
            summary="Resumen",
            content="Contenido",
        )
        attempt = DiagnosticAttempt.objects.create(
            user=self.user, completed_at=timezone.now()
        )
        DiagnosticResult.objects.create(
            attempt=attempt,
            suggested_unit=self.assigned_unit,
            maximum_score=10,
            scores={str(self.assigned_unit.id): 10},
            profile={
                "recommended_unit_ids": [self.assigned_unit.id, self.other_unit.id],
                "route_type": "prioritized",
                "dimensions": [
                    {"unit_id": self.assigned_unit.id, "priority": 1},
                    {"unit_id": self.other_unit.id, "priority": 2},
                ],
            },
        )
        self.quiz_questions = []
        for order in range(1, 6):
            question = ModuleQuizQuestion.objects.create(
                unit=self.assigned_unit, text=f"Pregunta {order}", order=order
            )
            correct = ModuleQuizOption.objects.create(
                question=question, label="Correcta", is_correct=True, order=1
            )
            wrong = ModuleQuizOption.objects.create(
                question=question, label="Incorrecta", is_correct=False, order=2
            )
            self.quiz_questions.append((question, correct, wrong))

    def test_course_returns_all_prioritized_modules_in_profile_order(self):
        response = self.client.get("/api/courses/units/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [unit["id"] for unit in response.data],
            [self.assigned_unit.id, self.other_unit.id],
        )
        self.assertEqual([unit["priority"] for unit in response.data], [1, 2])

    def test_complete_lesson(self):
        response = self.client.post(f"/api/courses/lessons/{self.lesson.id}/complete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["progress"], 100)

    def test_can_complete_a_lesson_in_a_secondary_prioritized_module(self):
        response = self.client.post(
            f"/api/courses/lessons/{self.other_lesson.id}/complete/"
        )
        self.assertEqual(response.status_code, 200)

    def test_cannot_complete_a_lesson_outside_prioritized_modules(self):
        response = self.client.post(
            f"/api/courses/lessons/{self.unassigned_lesson.id}/complete/"
        )
        self.assertEqual(response.status_code, 404)

    def test_completion_rejects_non_boolean_value(self):
        response = self.client.post(
            f"/api/courses/lessons/{self.lesson.id}/complete/",
            {"completed": "false"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_activity_requires_a_valid_decision(self):
        activity = Lesson.objects.create(
            unit=self.assigned_unit,
            title="Actividad",
            summary="Simulación",
            content="Caso",
            kind="activity",
            order=2,
            activity_options=[
                {"id": "reportar", "label": "Reportar", "feedback": "Bien"}
            ],
        )
        invalid = self.client.post(f"/api/courses/lessons/{activity.id}/complete/")
        self.assertEqual(invalid.status_code, 400)
        valid = self.client.post(
            f"/api/courses/lessons/{activity.id}/complete/",
            {"activity_choice": "reportar"},
            format="json",
        )
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(valid.data["feedback"], "Bien")

    def test_quiz_is_locked_until_learning_items_are_complete(self):
        response = self.client.post(
            "/api/courses/quiz/submit/",
            {"unit_id": self.assigned_unit.id, "answers": []},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_passing_quiz_generates_verifiable_pdf_certificate(self):
        self.client.post(f"/api/courses/lessons/{self.lesson.id}/complete/")
        answers = []
        for index, (question, correct, wrong) in enumerate(self.quiz_questions):
            answers.append(
                {
                    "question_id": question.id,
                    "option_id": correct.id if index < 4 else wrong.id,
                }
            )
        response = self.client.post(
            "/api/courses/quiz/submit/",
            {"unit_id": self.assigned_unit.id, "answers": answers},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["passed"])
        self.assertEqual(response.data["score_percentage"], 80)
        code = response.data["certificate"]["verification_code"]
        self.assertTrue(Certificate.objects.filter(verification_code=code).exists())

        download = self.client.get(f"/api/courses/certificates/{code}/download/")
        self.assertEqual(download.status_code, 200)
        self.assertEqual(download["Content-Type"], "application/pdf")
        self.assertTrue(download.content.startswith(b"%PDF"))

        self.client.force_authenticate(user=None)
        verification = self.client.get(f"/api/courses/certificates/verify/{code}/")
        self.assertEqual(verification.status_code, 200)
        self.assertTrue(verification.data["valid"])


class CourseRequiresDiagnosticTests(APITestCase):
    def test_course_requires_a_completed_diagnostic(self):
        user = get_user_model().objects.create_user(
            "demo", password="TestSegura2026!"
        )
        self.client.force_authenticate(user)
        response = self.client.get("/api/courses/units/")
        self.assertEqual(response.status_code, 403)
