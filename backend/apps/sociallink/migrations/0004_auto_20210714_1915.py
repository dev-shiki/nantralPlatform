# Generated by Django 3.2.4 on 2021-07-14 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sociallink', '0003_auto_20210703_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sociallink.socialnetwork', verbose_name='Type du lien'),
        ),
        migrations.AlterField(
            model_name='sociallink',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Slug du groupe'),
        ),
    ]
