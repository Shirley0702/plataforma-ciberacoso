from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_expand_user_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="age_range",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
