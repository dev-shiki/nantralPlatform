# Generated by Django 3.2.5 on 2021-11-17 22:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("liste", "0013_alter_liste_year"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="liste",
            options={
                "ordering": ["-year", "liste_type", "name"],
                "verbose_name": "Liste BDX",
                "verbose_name_plural": "Listes BDX",
            },
        ),
    ]
