from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diagnostics", "0002_scenario_based_diagnostic"),
    ]

    operations = [
        migrations.AddField(
            model_name="diagnosticresult",
            name="model_confidence",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="diagnosticresult",
            name="model_version",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="diagnosticresult",
            name="recommendation_method",
            field=models.CharField(
                choices=[
                    ("machine_learning", "Machine Learning"),
                    ("rule_fallback", "Respaldo basado en reglas"),
                ],
                default="rule_fallback",
                max_length=30,
            ),
        ),
    ]
