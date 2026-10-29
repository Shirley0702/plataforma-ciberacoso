from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_rename_display_name_to_full_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="age_range",
            field=models.CharField(
                blank=True,
                choices=[
                    ("under_18", "Menos de 18 años"),
                    ("18_20", "18 a 20 años"),
                    ("21_24", "21 a 24 años"),
                    ("25_29", "25 a 29 años"),
                    ("over_30", "30 años o más"),
                    ("undisclosed", "Prefiero no indicarlo"),
                ],
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="academic_program",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(blank=True, upload_to="profiles/avatars/"),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="bio",
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="university",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
