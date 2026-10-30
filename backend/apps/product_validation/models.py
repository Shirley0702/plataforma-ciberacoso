from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


RATING_VALIDATORS = [MinValueValidator(1), MaxValueValidator(5)]


class ParticipantFeedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_feedback",
    )
    app_version = models.CharField(max_length=40)
    ease_of_use = models.PositiveSmallIntegerField(validators=RATING_VALIDATORS)
    content_clarity = models.PositiveSmallIntegerField(validators=RATING_VALIDATORS)
    educational_usefulness = models.PositiveSmallIntegerField(validators=RATING_VALIDATORS)
    satisfaction = models.PositiveSmallIntegerField(validators=RATING_VALIDATORS)
    accessibility = models.PositiveSmallIntegerField(validators=RATING_VALIDATORS)
    open_comment = models.TextField(blank=True, max_length=1000)
    informed_consent = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "-id")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "app_version"),
                name="unique_feedback_per_user_and_version",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.app_version}"


class QualityAssessment(models.Model):
    class Characteristic(models.TextChoices):
        FUNCTIONAL_SUITABILITY = "functional_suitability", "Adecuación funcional"
        PERFORMANCE_EFFICIENCY = "performance_efficiency", "Eficiencia de desempeño"
        COMPATIBILITY = "compatibility", "Compatibilidad"
        INTERACTION_CAPABILITY = "interaction_capability", "Capacidad de interacción"
        RELIABILITY = "reliability", "Fiabilidad"
        SECURITY = "security", "Seguridad"
        MAINTAINABILITY = "maintainability", "Mantenibilidad"
        FLEXIBILITY = "flexibility", "Flexibilidad"
        SAFETY = "safety", "Protección ante riesgos"

    class Result(models.TextChoices):
        PASSED = "passed", "Cumple"
        PARTIAL = "partial", "Cumple parcialmente"
        FAILED = "failed", "No cumple"
        NOT_APPLICABLE = "not_applicable", "No aplica"

    app_version = models.CharField(max_length=40)
    characteristic = models.CharField(max_length=40, choices=Characteristic.choices)
    criterion = models.CharField(max_length=240)
    result = models.CharField(max_length=20, choices=Result.choices)
    evidence = models.TextField(
        help_text="Referencia verificable: prueba, informe, captura, métrica o incidencia."
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="quality_assessments",
    )
    assessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("app_version", "characteristic", "criterion")
        constraints = [
            models.UniqueConstraint(
                fields=("app_version", "characteristic", "criterion"),
                name="unique_quality_criterion_per_version",
            )
        ]

    def __str__(self):
        return f"{self.app_version} - {self.get_characteristic_display()}"
