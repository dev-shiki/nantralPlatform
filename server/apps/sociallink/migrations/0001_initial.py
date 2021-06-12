# Generated by Django 3.2.3 on 2021-06-12 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nom')),
                ('color', models.CharField(max_length=7, verbose_name='Couleur en hexadécimal')),
                ('icon_name', models.CharField(max_length=20, verbose_name="Nom Bootstrap de l'icône")),
            ],
            options={
                'verbose_name': 'Réseau Social',
                'verbose_name_plural': 'Réseaux Sociaux',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200, verbose_name='URL')),
                ('reseau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sociallink.socialnetwork')),
            ],
        ),
    ]
