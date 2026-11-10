from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0008_dynamic_learning_puzzles"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="interaction_type",
            field=models.CharField(
                choices=[
                    ("video", "Video de aprendizaje"),
                    ("guided", "Puzzle de pistas"),
                    ("decision", "Puzzle de caminos"),
                    ("matching", "Puzzle de conexiones"),
                    ("practice", "Laboratorio de respuestas"),
                    ("safety_plan", "Puzzle de secuencia segura"),
                ],
                default="guided",
                max_length=30,
            ),
        ),
    ]
