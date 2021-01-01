# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-11 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='friend',
            field=models.ManyToManyField(related_name='_member_friend_+', to='social.Member'),
        ),
    ]