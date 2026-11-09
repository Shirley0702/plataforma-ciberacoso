from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0006_interactive_learning_experiences"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="interaction_type",
            field=models.CharField(
                choices=[
                    ("video", "Microvideo interactivo"),
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
    ]
