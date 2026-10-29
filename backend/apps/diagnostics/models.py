from django.conf import settings
from django.db import models


class DiagnosticQuestion(models.Model):
    text = models.TextField()
    primary_unit = models.ForeignKey(
        "courses.CourseUnit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diagnostic_questions",
    )
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.text


class DiagnosticOption(models.Model):
    question = models.ForeignKey(
        DiagnosticQuestion, on_delete=models.CASCADE, related_name="options"
    )
    label = models.TextField()
    destination_unit = models.ForeignKey(
        "courses.CourseUnit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diagnostic_options",
    )
    weight = models.PositiveSmallIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.question_id}: {self.label}"


class DiagnosticAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diagnostic_attempts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Intento {self.pk} - {self.user}"


class DiagnosticAnswer(models.Model):
    attempt = models.ForeignKey(
        DiagnosticAttempt, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(DiagnosticQuestion, on_delete=models.PROTECT)
    option = models.ForeignKey(DiagnosticOption, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("attempt", "question"), name="unique_answer_per_question"
            )
        ]


class DiagnosticResult(models.Model):
    class RecommendationMethod(models.TextChoices):
        MACHINE_LEARNING = "machine_learning", "Machine Learning"
        RULE_FALLBACK = "rule_fallback", "Respaldo basado en reglas"

    attempt = models.OneToOneField(
        DiagnosticAttempt, on_delete=models.CASCADE, related_name="result"
    )
    scores = models.JSONField(default=dict)
    suggested_unit = models.ForeignKey(
        "courses.CourseUnit",
        on_delete=models.PROTECT,
        related_name="diagnostic_results",
    )
    maximum_score = models.PositiveIntegerField(default=0)
    recommendation_method = models.CharField(
        max_length=30,
        choices=RecommendationMethod.choices,
        default=RecommendationMethod.RULE_FALLBACK,
    )
    model_version = models.CharField(max_length=80, blank=True)
    model_confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attempt.user}: {self.suggested_unit}"
