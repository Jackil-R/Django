# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_auto_20160216_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following', models.ManyToManyField(to='social.Requests')),
            ],
        ),
    ]