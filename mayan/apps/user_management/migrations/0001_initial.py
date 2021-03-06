# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-26 10:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def add_user_options_to_existing_users(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    UserOptions = apps.get_model(
        app_label='user_management', model_name='UserOptions'
    )

    for user in User.objects.using(schema_editor.connection.alias).all():
        UserOptions.objects.using(
            schema_editor.connection.alias
        ).create(user=user)


def remove_user_options_from_existing_users(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    UserOptions = apps.get_model(
        app_label='user_management', model_name='UserOptions'
    )

    for user in User.objects.using(schema_editor.connection.alias).all():
        UserOptions.objects.using(
            schema_editor.connection.alias
        ).filter(user=user).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_password_change', models.BooleanField(default=False, verbose_name='Forbid this user from changing their password.')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_options', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User settings',
                'verbose_name_plural': 'Users settings',
            },
        ),
        migrations.RunPython(
            code=add_user_options_to_existing_users,
            reverse_code=remove_user_options_from_existing_users
        ),
    ]
