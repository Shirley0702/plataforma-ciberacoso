from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.diagnostics.models import DiagnosticAttempt, DiagnosticResult
from initial_data.catalog.course_units import COURSE_UNITS

from .models import (
    Certificate,
    CourseProgress,
    CourseUnit,
    Lesson,
    ModuleQuizOption,
    ModuleQuizQuestion,
)


class CourseCatalogTests(SimpleTestCase):
    def test_every_unit_contains_the_six_learning_experiences(self):
        expected_types = {
            "video",
            "guided",
            "decision",
            "matching",
            "practice",
            "safety_plan",
        }
        self.assertEqual(len(COURSE_UNITS), 5)
        for unit in COURSE_UNITS:
            self.assertEqual(len(unit["learning_items"]), 6)
            self.assertEqual(
                {item["interaction_type"] for item in unit["learning_items"]},
                expected_types,
                msg=unit["slug"],
            )

    def test_units_have_specific_quizzes_and_no_free_text_interactions(self):
        question_sets = []
        allowed_visuals = {
            "pause",
            "document",
            "support",
            "compass",
            "stop",
            "chat",
            "help",
            "lock",
            "report",
            "observe",
            "university",
            "emergency",
        }
        allowed_config_keys = {
            "cards",
            "options",
            "items",
            "completion_message",
            "completion_feedback",
            "privacy_note",
            "video_url",
            "video_watch_url",
            "video_title",
            "source_label",
        }
        for unit in COURSE_UNITS:
            self.assertEqual(len(unit["quiz"]), 5)
            question_sets.append(tuple(question["text"] for question in unit["quiz"]))
            for item in unit["learning_items"]:
                self.assertTrue(
                    set(item["interaction_config"]).issubset(allowed_config_keys)
                )
                if item["interaction_type"] == "safety_plan":
                    puzzle_items = item["interaction_config"]["items"]
                    self.assertEqual(len(puzzle_items), 4)
                    self.assertTrue(
                        all(
                            puzzle_item.get("visual") in allowed_visuals
                            for puzzle_item in puzzle_items
                        )
                    )
        self.assertEqual(len(set(question_sets)), len(COURSE_UNITS))


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

    def test_consequence_puzzle_requires_exploring_every_path(self):
        activity = Lesson.objects.create(
            unit=self.assigned_unit,
            title="Actividad",
            summary="Simulación",
            content="Caso",
            interaction_type=Lesson.InteractionType.DECISION,
            order=2,
            interaction_config={
                "options": [
                    {"id": "reportar", "label": "Reportar", "feedback": "Bien"}
                ]
            },
        )
        invalid = self.client.post(f"/api/courses/lessons/{activity.id}/complete/")
        self.assertEqual(invalid.status_code, 400)
        malformed = self.client.post(
            f"/api/courses/lessons/{activity.id}/complete/",
            {"interaction_response": ["reportar"]},
            format="json",
        )
        self.assertEqual(malformed.status_code, 400)
        incomplete = self.client.post(
            f"/api/courses/lessons/{activity.id}/complete/",
            {
                "interaction_response": {
                    "selected_items": [],
                    "private_story": "Este dato no debe almacenarse",
                }
            },
            format="json",
        )
        self.assertEqual(incomplete.status_code, 400)
        valid = self.client.post(
            f"/api/courses/lessons/{activity.id}/complete/",
            {
                "interaction_response": {
                    "selected_items": ["reportar"],
                    "private_story": "Este dato no debe almacenarse",
                }
            },
            format="json",
        )
        self.assertEqual(valid.status_code, 200)
        progress = CourseProgress.objects.get(user=self.user, lesson=activity)
        self.assertEqual(progress.interaction_response, {"selected_items": ["reportar"]})

    def test_matching_puzzle_requires_every_correct_connection(self):
        matching = Lesson.objects.create(
            unit=self.assigned_unit,
            title="Puzzle de conexiones",
            summary="Señales observables",
            content="Conecta cada señal",
            interaction_type=Lesson.InteractionType.MATCHING,
            order=2,
            interaction_config={
                "items": [
                    {"id": "contexto", "label": "Conservar el contexto"},
                    {"id": "apoyo", "label": "Buscar apoyo"},
                ],
                "completion_feedback": "Lista completada",
            },
        )
        incomplete = self.client.post(
            f"/api/courses/lessons/{matching.id}/complete/",
            {"interaction_response": {"matches": {"contexto": "apoyo"}}},
            format="json",
        )
        self.assertEqual(incomplete.status_code, 400)

        valid = self.client.post(
            f"/api/courses/lessons/{matching.id}/complete/",
            {
                "interaction_response": {
                    "matches": {"apoyo": "apoyo", "contexto": "contexto"},
                    "student_name": "No guardar",
                }
            },
            format="json",
        )
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(valid.data["feedback"], "Lista completada")
        progress = CourseProgress.objects.get(user=self.user, lesson=matching)
        self.assertEqual(
            progress.interaction_response,
            {"matches": {"contexto": "contexto", "apoyo": "apoyo"}},
        )

    def test_video_requires_watch_confirmation_without_storing_free_text(self):
        video = Lesson.objects.create(
            unit=self.assigned_unit,
            title="Microvideo",
            summary="Resumen",
            content="Contenido",
            interaction_type=Lesson.InteractionType.VIDEO,
            order=2,
            interaction_config={
                "video_url": "https://www.youtube-nocookie.com/embed/example",
            },
        )
        invalid = self.client.post(f"/api/courses/lessons/{video.id}/complete/")
        self.assertEqual(invalid.status_code, 400)

        valid = self.client.post(
            f"/api/courses/lessons/{video.id}/complete/",
            {
                "interaction_response": {
                    "watched": True,
                    "personal_detail": "No guardar",
                }
            },
            format="json",
        )
        self.assertEqual(valid.status_code, 200)
        progress = CourseProgress.objects.get(user=self.user, lesson=video)
        self.assertEqual(progress.interaction_response, {"watched": True})

    def test_ordering_puzzle_requires_the_exact_safe_sequence(self):
        puzzle = Lesson.objects.create(
            unit=self.assigned_unit,
            title="Puzzle de secuencia segura",
            summary="Ordena los pasos",
            content="Aprende una respuesta gradual",
            interaction_type=Lesson.InteractionType.SAFETY_PLAN,
            order=3,
            interaction_config={
                "items": [
                    {"id": "pausa", "label": "Hacer una pausa"},
                    {"id": "evidencia", "label": "Conservar hechos"},
                    {"id": "apoyo", "label": "Buscar apoyo"},
                ],
                "completion_feedback": "Secuencia aprendida",
            },
        )
        incorrect = self.client.post(
            f"/api/courses/lessons/{puzzle.id}/complete/",
            {"interaction_response": {"selected_items": ["apoyo", "evidencia", "pausa"]}},
            format="json",
        )
        self.assertEqual(incorrect.status_code, 400)

        valid = self.client.post(
            f"/api/courses/lessons/{puzzle.id}/complete/",
            {
                "interaction_response": {
                    "selected_items": ["pausa", "evidencia", "apoyo"],
                    "private_story": "No debe guardarse",
                }
            },
            format="json",
        )
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(valid.data["feedback"], "Secuencia aprendida")
        progress = CourseProgress.objects.get(user=self.user, lesson=puzzle)
        self.assertEqual(
            progress.interaction_response,
            {"selected_items": ["pausa", "evidencia", "apoyo"]},
        )

    def test_guided_exploration_does_not_store_personal_content(self):
        response = self.client.post(
            f"/api/courses/lessons/{self.lesson.id}/complete/",
            {"interaction_response": {"free_text": "Información privada"}},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        progress = CourseProgress.objects.get(user=self.user, lesson=self.lesson)
        self.assertEqual(progress.interaction_response, {})

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
