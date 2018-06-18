# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-01 10:32
from __future__ import unicode_literals

from django.db import migrations


def modify_editors_user_group(apps, schema_editor):
    """
    Rename 'Edit Collections and Folders' user group to 'Editors'.
    """
    Group = apps.get_model('auth', 'Group')
    editors_group = Group.objects.get(name='Edit Collections and Folders')
    editors_group.name = 'Editors'
    editors_group.save()


def add_managers_user_group(apps, schema_editor):
    """
    Create 'Managers' user group with permissions to add and edit
    collections and dips.
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    managers_group, created = Group.objects.get_or_create(name='Managers')
    if created:
        permissions = Permission.objects.filter(codename__in=(
            'add_user', 'change_user', 'delete_user',
        ))
        for permission in permissions:
            managers_group.permissions.add(permission)
        managers_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dips', '0002_add_user_group'),
    ]

    operations = [
        migrations.RunPython(modify_editors_user_group),
        migrations.RunPython(add_managers_user_group),
    ]
