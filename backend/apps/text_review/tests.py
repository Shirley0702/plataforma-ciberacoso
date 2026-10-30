from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from apps.courses.models import CourseUnit
from apps.diagnostics.models import DiagnosticAttempt, DiagnosticResult

from .ml import classify_text, train_and_save_classifier
from .ml.dataset import load_training_dataset
from .ml.classifier import split_dataset
from .models import TextReview
from .recommendations import build_recommendations, detect_contexts


class PersonalizedRecommendationTests(SimpleTestCase):
    def test_detects_multiple_contexts_without_storing_the_original_text(self):
        contexts = detect_contexts(
            "El tutor me amenaza con publicar una foto y lo repite todos los días."
        )

        self.assertEqual(contexts, ["pressure", "privacy", "repetition", "authority"])

    def test_high_attention_prioritizes_safety_and_context(self):
        recommendations = build_recommendations(
            needs_attention=True,
            attention_level="high",
            context_keys=["pressure"],
            recommended_unit=None,
        )

        self.assertIn("Prioriza tu seguridad", recommendations[0])
        self.assertTrue(any("amenaza" in item for item in recommendations))


class TextReviewModelTests(APITestCase):
    def test_training_compares_models_and_keeps_required_metrics(self):
        artifact = train_and_save_classifier()

        self.assertEqual(len(artifact["validation_evaluations"]), 3)
        self.assertIn(
            artifact["selected_algorithm"],
            artifact["validation_evaluations"],
        )
        self.assertEqual(artifact["selection_metric"], "validation_f1")
        self.assertEqual(sum(artifact["split_sizes"].values()), artifact["dataset_size"])
        self.assertGreater(artifact["split_sizes"]["train"], artifact["split_sizes"]["test"])
        self.assertEqual(artifact["training_source"]["name"], "CLANDESTINO")
        self.assertEqual(artifact["training_source"]["license"], "MIT")
        self.assertEqual(artifact["dataset_source_sizes"]["training_examples.csv"], 706)
        self.assertEqual(artifact["dataset_source_sizes"]["domain_examples.csv"], 120)
        for metrics in artifact["validation_evaluations"].values():
            self.assertEqual(
                set(metrics),
                {"accuracy", "precision", "recall", "f1", "confusion_matrix"},
            )
            self.assertEqual(len(metrics["confusion_matrix"]), 2)
        self.assertEqual(
            set(artifact["test_metrics"]),
            {"accuracy", "precision", "recall", "f1", "confusion_matrix"},
        )
        self.assertEqual(artifact["eda_summary"]["quality_checks"]["empty_texts"], 0)
        self.assertEqual(
            artifact["eda_summary"]["quality_checks"]["duplicate_normalized_texts"],
            0,
        )

        attention = classify_text(
            "Me amenaza con publicar información privada si no respondo."
        )
        neutral = classify_text(
            "La profesora explicó la rúbrica y respondió las preguntas."
        )
        self.assertEqual(attention["label"], "attention")
        self.assertEqual(neutral["label"], "neutral")

    def test_split_reserves_independent_validation_and_test_sets(self):
        dataset = load_training_dataset()
        split = split_dataset(dataset)

        train = set(split.train_texts)
        validation = set(split.validation_texts)
        test = set(split.test_texts)
        self.assertFalse(train & validation)
        self.assertFalse(train & test)
        self.assertFalse(validation & test)
        self.assertEqual(len(train | validation | test), len(dataset.texts))
        for labels in (
            split.train_labels,
            split.validation_labels,
            split.test_labels,
        ):
            self.assertEqual(set(labels), {"attention", "neutral"})


class TextReviewApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="participant",
            password="TestSegura2026!",
        )
        self.unit = CourseUnit.objects.create(
            title="Convivencia Digital",
            slug="convivencia-digital",
            description="Herramientas prácticas.",
            order=1,
        )
        attempt = DiagnosticAttempt.objects.create(user=self.user)
        DiagnosticResult.objects.create(
            attempt=attempt,
            suggested_unit=self.unit,
            maximum_score=10,
        )
        self.client.force_authenticate(self.user)

    def test_review_combines_text_with_latest_diagnostic_without_storing_text(self):
        sensitive_text = (
            "Me envían mensajes ofensivos todos los días y aunque pedí que paren continúan."
        )

        with patch(
            "apps.text_review.use_cases.review_text.classify_text",
            return_value={
                "label": "attention",
                "attention_score": 0.82,
                "version": "spanish-text-review-v3",
                "algorithm": "logistic_regression",
            },
        ):
            response = self.client.post(
                "/api/text-reviews/review/",
                {"text": sensitive_text},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["possible_signals"])
        self.assertEqual(response.data["recommended_unit"]["id"], self.unit.id)
        self.assertNotIn("text", response.data)
        review = TextReview.objects.get()
        self.assertEqual(review.character_count, len(sensitive_text))
        self.assertIn("repetition", review.context_signals)
        self.assertIn("Situación repetida", response.data["contexts_considered"])
        self.assertFalse(any(field.name == "text" for field in TextReview._meta.fields))

    def test_review_requires_a_detailed_text(self):
        response = self.client.post(
            "/api/text-reviews/review/",
            {"text": "No sé"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_requires_a_completed_diagnostic(self):
        user_without_diagnostic = get_user_model().objects.create_user(
            username="new-participant",
            password="TestSegura2026!",
        )
        self.client.force_authenticate(user_without_diagnostic)

        response = self.client.post(
            "/api/text-reviews/review/",
            {"text": "Quiero revisar una situación que ocurrió en el grupo de clase."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_latest_review_returns_null_before_first_review(self):
        response = self.client.get("/api/text-reviews/latest/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
