from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_email_verification"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofile",
            old_name="display_name",
            new_name="full_name",
        ),
    ]
