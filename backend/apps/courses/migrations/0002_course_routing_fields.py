from django.db import migrations, models


def populate_unique_slugs(apps, schema_editor):
    CourseUnit = apps.get_model("courses", "CourseUnit")
    for unit in CourseUnit.objects.all():
        unit.slug = f"modulo-{unit.pk}"
        unit.content_url = "/curso"
        unit.save(update_fields=("slug", "content_url"))


class Migration(migrations.Migration):
    dependencies = [("courses", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="courseunit",
            name="slug",
            field=models.SlugField(
                blank=True, db_index=False, default="", max_length=80
            ),
        ),
        migrations.AddField(
            model_name="courseunit",
            name="content_url",
            field=models.CharField(default="/curso", max_length=255),
        ),
        migrations.RunPython(populate_unique_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="courseunit",
            name="slug",
            field=models.SlugField(max_length=80, unique=True),
        ),
    ]
