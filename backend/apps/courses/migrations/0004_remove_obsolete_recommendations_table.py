from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("courses", "0003_microlearning_and_certificates")]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS recommendations_recommendation",
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
