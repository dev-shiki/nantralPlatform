# Generated by Django 3.2.5 on 2021-11-12 16:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0005_auto_20210801_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titre')),
                ('body', models.CharField(max_length=255, verbose_name='Corps')),
                ('url', models.URLField(max_length=255, verbose_name='Cible')),
                ('group', models.SlugField(verbose_name='Groupe')),
                ('action1_label', models.CharField(blank=True, max_length=20, null=True, verbose_name='Action 1 - Label')),
                ('action1_url', models.URLField(blank=True, max_length=255, null=True, verbose_name='Action 1 - Cible')),
                ('action2_label', models.CharField(blank=True, max_length=20, null=True, verbose_name='Action 1 - Label')),
                ('action2_url', models.URLField(blank=True, max_length=255, null=True, verbose_name='Action 1 - Cible')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de création')),
                ('high_priority', models.BooleanField(default=False, verbose_name='Prioritaire')),
            ],
        ),
        migrations.CreateModel(
            name='ReceivedNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False, verbose_name='Vu')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notification.notification')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'verbose_name': 'Notification reçue',
                'verbose_name_plural': 'Notifications reçues',
                'unique_together': {('student', 'notification')},
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='receivers',
            field=models.ManyToManyField(related_name='notification_set', through='notification.ReceivedNotification', to='student.Student'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.SlugField(verbose_name='Groupe')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'verbose_name': 'Abonnement',
                'unique_together': {('student', 'group')},
            },
        ),
    ]
