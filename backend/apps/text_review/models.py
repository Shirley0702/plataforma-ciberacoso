from django.conf import settings
from django.db import models


class TextReview(models.Model):
    class Classification(models.TextChoices):
        NO_CLEAR_SIGNALS = "no_clear_signals", "Sin señales claras"
        NEEDS_ATTENTION = "needs_attention", "Requiere atención"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="text_reviews",
    )
    diagnostic_result = models.ForeignKey(
        "diagnostics.DiagnosticResult",
        on_delete=models.SET_NULL,
        null=True,
        related_name="text_reviews",
    )
    recommended_unit = models.ForeignKey(
        "courses.CourseUnit",
        on_delete=models.SET_NULL,
        null=True,
        related_name="text_reviews",
    )
    classification = models.CharField(
        max_length=30,
        choices=Classification.choices,
    )
    attention_score = models.FloatField()
    attention_level = models.CharField(max_length=20)
    model_version = models.CharField(max_length=80)
    character_count = models.PositiveIntegerField()
    context_signals = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-id")

    def __str__(self):
        return f"Revisión {self.pk} - {self.user}"

