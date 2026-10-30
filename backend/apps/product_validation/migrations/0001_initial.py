import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="ParticipantFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("app_version", models.CharField(max_length=40)),
                ("ease_of_use", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("content_clarity", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("educational_usefulness", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("satisfaction", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("accessibility", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("open_comment", models.TextField(blank=True, max_length=1000)),
                ("informed_consent", models.BooleanField(default=False)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="product_feedback", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-updated_at", "-id")},
        ),
        migrations.CreateModel(
            name="QualityAssessment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("app_version", models.CharField(max_length=40)),
                ("characteristic", models.CharField(choices=[("functional_suitability", "Adecuación funcional"), ("performance_efficiency", "Eficiencia de desempeño"), ("compatibility", "Compatibilidad"), ("interaction_capability", "Capacidad de interacción"), ("reliability", "Fiabilidad"), ("security", "Seguridad"), ("maintainability", "Mantenibilidad"), ("flexibility", "Flexibilidad"), ("safety", "Protección ante riesgos")], max_length=40)),
                ("criterion", models.CharField(max_length=240)),
                ("result", models.CharField(choices=[("passed", "Cumple"), ("partial", "Cumple parcialmente"), ("failed", "No cumple"), ("not_applicable", "No aplica")], max_length=20)),
                ("evidence", models.TextField(help_text="Referencia verificable: prueba, informe, captura, métrica o incidencia.")),
                ("assessed_at", models.DateTimeField(auto_now_add=True)),
                ("evaluator", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="quality_assessments", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("app_version", "characteristic", "criterion")},
        ),
        migrations.AddConstraint(
            model_name="participantfeedback",
            constraint=models.UniqueConstraint(fields=("user", "app_version"), name="unique_feedback_per_user_and_version"),
        ),
        migrations.AddConstraint(
            model_name="qualityassessment",
            constraint=models.UniqueConstraint(fields=("app_version", "characteristic", "criterion"), name="unique_quality_criterion_per_version"),
        ),
    ]
