# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 10:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils import timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='created_at',
            field=models.DateTimeField(default=timezone.now),
        ),
        migrations.AlterField(
            model_name='thread',
            name='created_at',
            field=models.DateTimeField(default=timezone.now),
        ),
    ]
