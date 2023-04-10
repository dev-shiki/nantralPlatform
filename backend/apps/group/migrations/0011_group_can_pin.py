# Generated by Django 4.1.4 on 2023-03-31 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0010_group_grouptype_tag_membership_label_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='can_pin',
            field=models.BooleanField(default=False, help_text='Whether admin members can pin a post', verbose_name='Can pin'),
        ),
    ]
