# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_auto_20160215_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='accept',
            field=models.BooleanField(default=True),
        ),
    ]
