import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_course_routing_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="kind",
            field=models.CharField(
                choices=[("lesson", "Lección"), ("activity", "Actividad interactiva")],
                default="lesson",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="duration_minutes",
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="lesson",
            name="activity_prompt",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="lesson",
            name="activity_options",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="courseprogress",
            name="activity_response",
            field=models.CharField(blank=True, max_length=260),
        ),
        migrations.CreateModel(
            name="ModuleQuizQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("order", models.PositiveIntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
                ("unit", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_questions", to="courses.courseunit")),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="ModuleQuizOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.TextField()),
                ("is_correct", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="courses.modulequizquestion")),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="ModuleQuizAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score_percentage", models.PositiveSmallIntegerField()),
                ("passed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("unit", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="quiz_attempts", to="courses.courseunit")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_attempts", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at", "-id")},
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("verification_code", models.CharField(max_length=50, unique=True)),
                ("issued_at", models.DateTimeField(auto_now_add=True)),
                ("unit", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="certificates", to="courses.courseunit")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="certificates", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="certificate",
            constraint=models.UniqueConstraint(fields=("user", "unit"), name="unique_certificate_per_user_unit"),
        ),
    ]
