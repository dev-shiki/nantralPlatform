# Generated by Django 3.0.5 on 2020-06-26 18:45

import apps.utils.upload
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nom du groupe')),
                ('description', models.TextField(blank=True, verbose_name='Description du groupe')),
                ('slug', models.SlugField(blank=True, max_length=40, unique=True)),
                ('parent', models.SlugField(blank=True, max_length=40, null=True)),
                ('bdx_type', models.CharField(choices=[('BDA', 'Bureau des Arts'), ('BDE', 'Bureau des Élèves'), ('BDS', 'Bureau des Sports'), ('Asso', 'Association')], max_length=60, verbose_name='Type de club BDX')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=apps.utils.upload.PathAndRename('groups/logo/club'), verbose_name='Logo du club')),
                ('admins', models.ManyToManyField(related_name='club_admins', to='student.Student', verbose_name='Administrateur.rice.s du groupe')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Liste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nom du groupe')),
                ('description', models.TextField(blank=True, verbose_name='Description du groupe')),
                ('slug', models.SlugField(blank=True, max_length=40, unique=True)),
                ('parent', models.SlugField(blank=True, max_length=40, null=True)),
                ('liste_type', models.CharField(choices=[('BDA', 'Bureau des Arts'), ('BDE', 'Bureau des Élèves'), ('BDS', 'Bureau des Sports')], max_length=60, verbose_name='Type de liste BDX')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Année de la liste')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=apps.utils.upload.PathAndRename('groups/logo/liste'), verbose_name='Logo de la liste')),
                ('admins', models.ManyToManyField(related_name='liste_admins', to='student.Student', verbose_name='Administrateur.rice.s du groupe')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NamedMembershipList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(blank=True, max_length=200, verbose_name='Poste occupé')),
                ('liste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.Liste')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
            options={
                'unique_together': {('function', 'student', 'liste')},
            },
        ),
        migrations.CreateModel(
            name='NamedMembershipClub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(blank=True, max_length=200, verbose_name='Poste occupé')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Année du poste')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.Club')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
            options={
                'unique_together': {('function', 'year', 'student', 'club')},
            },
        ),
        migrations.AddField(
            model_name='liste',
            name='members',
            field=models.ManyToManyField(through='group.NamedMembershipList', to='student.Student'),
        ),
        migrations.AddField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(through='group.NamedMembershipClub', to='student.Student'),
        ),
    ]
