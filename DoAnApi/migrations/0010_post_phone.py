# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DoAnApi', '0009_auto_20171123_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
