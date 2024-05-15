# Generated by Django 4.2.5 on 2023-09-26 14:02


from django.db import migrations, models

import django_ckeditor_5.fields


def copy_data(apps, schema_editor):
    Event = apps.get_model("event", "event")  # noqa: N806
    for obj in Event.objects.all():
        if not obj.title_fr:
            obj.title_fr = obj.title
            obj.save()
        if not obj.description_fr:
            obj.description_fr = obj.description
            obj.save()


def reverse_copy_data(apps, schema_editor):
    return


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0016_alter_event_image"),
    ]
    operations = [
        migrations.AddField(
            model_name="event",
            name="description_en",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="description_fr",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="title_en",
            field=models.CharField(
                max_length=200,
                null=True,
                verbose_name="Title",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="title_fr",
            field=models.CharField(
                max_length=200,
                null=True,
                verbose_name="Title",
            ),
        ),
        migrations.RunPython(copy_data, reverse_code=reverse_copy_data),
    ]
