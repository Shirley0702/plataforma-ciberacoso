import django.db.models.deletion
from django.db import migrations, models


def clear_incompatible_attempts(apps, schema_editor):
    apps.get_model("diagnostics", "DiagnosticAttempt").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_course_routing_fields"),
        ("diagnostics", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="diagnosticquestion",
            name="primary_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="diagnostic_questions",
                to="courses.courseunit",
            ),
        ),
        migrations.RemoveField(model_name="diagnosticquestion", name="dimension"),
        migrations.AlterField(
            model_name="diagnosticquestion",
            name="text",
            field=models.TextField(),
        ),
        migrations.RenameField(
            model_name="diagnosticoption", old_name="score", new_name="weight"
        ),
        migrations.AddField(
            model_name="diagnosticoption",
            name="destination_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="diagnostic_options",
                to="courses.courseunit",
            ),
        ),
        migrations.AlterField(
            model_name="diagnosticoption",
            name="label",
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name="diagnosticresult",
            name="maximum_score",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="diagnosticresult",
            name="suggested_unit",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="diagnostic_results",
                to="courses.courseunit",
            ),
        ),
        migrations.RunPython(clear_incompatible_attempts, migrations.RunPython.noop),
        migrations.RemoveField(model_name="diagnosticresult", name="level"),
        migrations.AlterField(
            model_name="diagnosticresult",
            name="suggested_unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="diagnostic_results",
                to="courses.courseunit",
            ),
        ),
    ]
