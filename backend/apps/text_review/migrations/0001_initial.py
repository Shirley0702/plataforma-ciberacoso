import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0005_remove_courseunit_content_url"),
        ("diagnostics", "0003_add_ml_recommendation_metadata"),
    ]

    operations = [
        migrations.CreateModel(
            name="TextReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "classification",
                    models.CharField(
                        choices=[
                            ("no_clear_signals", "Sin señales claras"),
                            ("needs_attention", "Requiere atención"),
                        ],
                        max_length=30,
                    ),
                ),
                ("attention_score", models.FloatField()),
                ("attention_level", models.CharField(max_length=20)),
                ("model_version", models.CharField(max_length=80)),
                ("character_count", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "diagnostic_result",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="text_reviews",
                        to="diagnostics.diagnosticresult",
                    ),
                ),
                (
                    "recommended_unit",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="text_reviews",
                        to="courses.courseunit",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="text_reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("-created_at", "-id")},
        ),
    ]
