from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("courses", "0004_remove_obsolete_recommendations_table")]

    operations = [
        migrations.RemoveField(
            model_name="courseunit",
            name="content_url",
        )
    ]
