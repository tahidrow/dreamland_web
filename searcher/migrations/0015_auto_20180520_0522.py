# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-20 05:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searcher', '0014_weapon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weapon',
            old_name='weaponClass',
            new_name='wclass',
        ),
    ]
