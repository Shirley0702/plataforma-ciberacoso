from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("text_review", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="textreview",
            name="context_signals",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
