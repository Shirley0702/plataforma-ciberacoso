from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diagnostics", "0003_add_ml_recommendation_metadata"),
    ]

    operations = [
        migrations.AddField(
            model_name="diagnosticresult",
            name="scoring_version",
            field=models.CharField(default="weighted-scores-v1", max_length=40),
        ),
        migrations.RemoveField(
            model_name="diagnosticresult",
            name="model_confidence",
        ),
        migrations.RemoveField(
            model_name="diagnosticresult",
            name="model_version",
        ),
        migrations.RemoveField(
            model_name="diagnosticresult",
            name="recommendation_method",
        ),
    ]
