# Generated by Django 3.0.14 on 2021-04-20 17:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20210420_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 20, 19, 41, 24, 28879), verbose_name='Date de publication'),
        ),
    ]
