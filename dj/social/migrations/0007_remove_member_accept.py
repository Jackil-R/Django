# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_member_accept'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='accept',
        ),
    ]