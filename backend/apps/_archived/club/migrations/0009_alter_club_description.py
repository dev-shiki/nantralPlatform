# Generated by Django 3.2.3 on 2021-06-19 21:22

from django.db import migrations

import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("club", "0008_club_social"),
    ]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="description",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                verbose_name="Description du groupe",
            ),
        ),
    ]
