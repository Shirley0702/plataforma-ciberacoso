from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diagnostics", "0004_use_weighted_scoring"),
    ]

    operations = [
        migrations.AddField(
            model_name="diagnosticresult",
            name="profile",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="diagnosticresult",
            name="scoring_version",
            field=models.CharField(
                default="multidimensional-profile-v2", max_length=40
            ),
        ),
    ]
