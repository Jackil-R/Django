# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 13:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_auto_20160216_1310'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Requests',
            new_name='Request',
        ),
    ]
