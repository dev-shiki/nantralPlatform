# Generated by Django 4.1.7 on 2023-02-22 11:10

import django.db.models.deletion
from django.db import migrations, models

import django_ckeditor_5.fields

import apps.utils.slug
import apps.utils.upload


class Migration(migrations.Migration):

    dependencies = [
        ('sociallink', '0005_alter_sociallink_label_alter_sociallink_url'),
        ('student', '0006_alter_student_faculty'),
        ('group', '0009_auto_20210831_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('short_name', models.CharField(blank=True, help_text='This name will be used in the list of groups.', max_length=100, verbose_name='Short name')),
                ('children_label', models.CharField(default='Sous-groupes', max_length=50, verbose_name='Children groups label')),
                ('lock_memberships', models.BooleanField(default=False, help_text='Users cannot add themselves as members of this group.', verbose_name='Lock memberships')),
                ('priority', models.IntegerField(default=0, verbose_name='Priority')),
                ('creation_year', models.IntegerField(blank=True, help_text='The year the group has been created.', null=True, verbose_name='Year of creation')),
                ('slug', models.SlugField(blank=True, max_length=40, unique=True)),
                ('archived', models.BooleanField(default=False, help_text='An archived group cannot have new members and is hidden from the displayed list.', verbose_name='Archived group')),
                ('private', models.BooleanField(default=False, help_text='A private group is only visible by group members.', verbose_name='Private group')),
                ('public', models.BooleanField(default=False, help_text='If ticked, the group page can be seen by everyone, including non-authenticated users. Members, events and posts still however hidden.', verbose_name='Public group')),
                ('summary', models.CharField(blank=True, max_length=500, verbose_name='Summary')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Description')),
                ('meeting_place', models.CharField(blank=True, max_length=50, verbose_name='Meeting place')),
                ('meeting_hour', models.CharField(blank=True, max_length=50, verbose_name='Meeting hours')),
                ('icon', models.ImageField(blank=True, help_text='Your icon will be displayed at 306x306 pixels.', null=True, upload_to=apps.utils.upload.PathAndRename('groups/logo'), verbose_name='Icon')),
                ('banner', models.ImageField(blank=True, help_text='Your banner will be displayed at 1320x492 pixels.', null=True, upload_to=apps.utils.upload.PathAndRename('groups/banniere'), verbose_name='Banner')),
                ('video1', models.URLField(blank=True, null=True, verbose_name='Video link 1')),
                ('video2', models.URLField(blank=True, null=True, verbose_name='Video link 2')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='student.student')),
            ],
            options={
                'verbose_name': 'groupe',
            },
            bases=(models.Model, apps.utils.slug.SlugModel),
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Type name')),
                ('slug', models.SlugField(max_length=10, primary_key=True, serialize=False)),
                ('icon', models.ImageField(blank=True, null=True, upload_to=apps.utils.upload.PathAndRename('groups/types'), verbose_name='Icon')),
                ('no_membership_dates', models.BooleanField(default=False, help_text='Do not ask dates for members.', verbose_name='No dates for memberships')),
                ('private_by_default', models.BooleanField(default=False, help_text='New groups are private by default.', verbose_name='Private by default')),
                ('sort_fields', models.CharField(default='-priority,short_name', help_text="Fields used to sort groups in the list, separated by ',' and without spaces. If categories are defined, you must also reflect them here.", max_length=100, verbose_name='Sort Fields')),
                ('category_expr', models.CharField(default="''", help_text='A python expression to get the category label.', max_length=200, verbose_name='Category expression')),
                ('sub_category_expr', models.CharField(default="''", help_text='A python expression to get the sub-category label.', max_length=200, verbose_name='Sub category expression')),
                ('hide_no_active_members', models.BooleanField(default=False, help_text="Hide groups where all 'end_date' from members are past.", verbose_name='Hide groups without active members')),
                ('can_create', models.BooleanField(default=False, verbose_name='Everyone can create new group')),
                ('extra_parents', models.ManyToManyField(blank=True, help_text='Children groups of these groups will be displayed in the list of all groups.', related_name='+', to='group.group', verbose_name='Additional parent groups')),
            ],
            options={
                'verbose_name': 'group type',
                'verbose_name_plural': 'group types',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tag Name')),
                ('group_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.grouptype', verbose_name='Type of group')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(blank=True, max_length=50, verbose_name='Summary')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('begin_date', models.DateField(null=True, verbose_name='Begin date')),
                ('end_date', models.DateField(null=True, verbose_name='End date')),
                ('priority', models.IntegerField(default=0, verbose_name='Priority')),
                ('admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('admin_request', models.BooleanField(default=False, verbose_name='Asked to become admin')),
                ('admin_request_messsage', models.TextField(blank=True, verbose_name='Request message')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_set', to='group.group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_set', to='student.student')),
            ],
            options={
                'verbose_name': 'membre',
                'ordering': ['group', '-priority', 'student'],
                'unique_together': {('student', 'group')},
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Label Name')),
                ('priority', models.IntegerField(default=0, verbose_name='Priority')),
                ('group_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.grouptype', verbose_name='Type of group')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='group_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.grouptype', verbose_name='Type of group'),
        ),
        migrations.AddField(
            model_name='group',
            name='label',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='group.label', verbose_name='Label'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='groups', through='group.Membership', to='student.student', verbose_name='Members'),
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='group.group', verbose_name='Parent group'),
        ),
        migrations.AddField(
            model_name='group',
            name='social_links',
            field=models.ManyToManyField(blank=True, related_name='+', to='sociallink.sociallink', verbose_name='Social networks'),
        ),
        migrations.AddField(
            model_name='group',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscriptions', to='student.student', verbose_name='Subscribers'),
        ),
        migrations.AddField(
            model_name='group',
            name='tags',
            field=models.ManyToManyField(blank=True, to='group.tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='group',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='student.student'),
        ),
    ]
