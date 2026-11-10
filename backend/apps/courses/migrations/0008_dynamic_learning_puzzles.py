from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0007_add_video_learning_experience"),
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
                    ("safety_plan", "Kit personal de apoyo"),
                ],
                default="guided",
                max_length=30,
            ),
        ),
    ]
