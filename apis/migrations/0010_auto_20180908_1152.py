# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-08 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0009_auto_20180908_0705'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='authy_id',
            field=models.CharField(default=0, max_length=24),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=0, max_length=24),
        ),
    ]
