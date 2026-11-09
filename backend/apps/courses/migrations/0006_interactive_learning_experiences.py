import json

from django.db import migrations, models


def prepare_interactive_data(apps, schema_editor):
    Lesson = apps.get_model("courses", "Lesson")
    CourseProgress = apps.get_model("courses", "CourseProgress")

    Lesson.objects.filter(kind="lesson").update(kind="guided")
    Lesson.objects.filter(kind="activity").update(kind="decision")
    for progress in CourseProgress.objects.all().iterator():
        response = (
            {"selected_option": progress.activity_response}
            if progress.activity_response
            else {}
        )
        progress.activity_response = json.dumps(response)
        progress.save(update_fields=("activity_response",))


def restore_legacy_data(apps, schema_editor):
    Lesson = apps.get_model("courses", "Lesson")
    CourseProgress = apps.get_model("courses", "CourseProgress")

    Lesson.objects.filter(kind="guided").update(kind="lesson")
    Lesson.objects.exclude(kind="lesson").update(kind="activity")
    for progress in CourseProgress.objects.all().iterator():
        try:
            response = json.loads(progress.activity_response or "{}")
        except (TypeError, json.JSONDecodeError):
            response = {}
        progress.activity_response = str(response.get("selected_option", ""))
        progress.save(update_fields=("activity_response",))


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0005_remove_courseunit_content_url"),
    ]

    operations = [
        migrations.RunPython(prepare_interactive_data, restore_legacy_data),
        migrations.RenameField(
            model_name="lesson",
            old_name="kind",
            new_name="interaction_type",
        ),
        migrations.RenameField(
            model_name="lesson",
            old_name="activity_prompt",
            new_name="interaction_prompt",
        ),
        migrations.RenameField(
            model_name="lesson",
            old_name="activity_options",
            new_name="interaction_config",
        ),
        migrations.RenameField(
            model_name="courseprogress",
            old_name="activity_response",
            new_name="interaction_response",
        ),
        migrations.AlterField(
            model_name="lesson",
            name="interaction_type",
            field=models.CharField(
                choices=[
                    ("guided", "Exploración guiada"),
                    ("decision", "Decisión con retroalimentación"),
                    ("checklist", "Lista interactiva"),
                    ("practice", "Práctica de respuesta"),
                    ("safety_plan", "Plan personal de seguridad"),
                ],
                default="guided",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="interaction_config",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="courseprogress",
            name="interaction_response",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
