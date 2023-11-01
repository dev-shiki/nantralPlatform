# Generated by Django 4.2.4 on 2023-09-16 14:54

from datetime import datetime

import django.db.models.deletion
from django.db import migrations, models
from django.utils import timezone


def migrate_temporary_accounts(apps, schema_editor):
    TemporaryAccessRequest: models.Model = apps.get_model(
        "account", "TemporaryAccessRequest"
    )
    IdRegistration: models.Model = apps.get_model("account", "IdRegistration")
    invitation = IdRegistration.objects.first()

    for temp_account in TemporaryAccessRequest.objects.all():
        temp_account.user.invitation = invitation
        temp_account.user.save()


def migrate_temporary_accounts_back(apps, schema_editor):
    User: models.Model = apps.get_model("account", "User")
    TemporaryAccessRequest: models.Model = apps.get_model(
        "account", "TemporaryAccessRequest"
    )

    for user in User.objects.all():
        if user.invitation is not None:
            TemporaryAccessRequest.objects.create(
                user=user,
                final_email=user.email_next,
                domain="nantral-platform.fr",
                approved_until=user.invitation.expires_at,
                date=user.date_joined,
                approved=True,
                mail_valid=user.is_email_valid,
            )


def change_mail_valid(apps, schema_editor):
    """Set active property to True for every user"""
    User: models.Model = apps.get_model("account", "User")
    for user in User.objects.all():
        user.is_email_valid = user.is_active
        user.active = True
        user.save()


def change_mail_valid_back(apps, schema_editor):
    User: models.Model = apps.get_model("account", "User")
    for user in User.objects.all():
        user.active = user.is_email_valid
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0009_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="idregistration",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime(
                    timezone.now().today().year,
                    10,
                    30,
                    23,
                    59,
                    tzinfo=timezone.get_current_timezone(),
                )
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="email_next",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="user",
            name="invitation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="account.idregistration",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="is_email_valid",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            migrate_temporary_accounts,
            reverse_code=migrate_temporary_accounts_back,
        ),
        migrations.RunPython(
            change_mail_valid, reverse_code=change_mail_valid_back
        ),
        migrations.DeleteModel(
            name="temporaryaccessrequest",
        ),
        migrations.RenameModel(
            old_name="IdRegistration",
            new_name="InvitationLink",
        ),
        migrations.AddField(
            model_name="invitationlink",
            name="description",
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
