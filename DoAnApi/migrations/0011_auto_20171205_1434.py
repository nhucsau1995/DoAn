# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 07:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DoAnApi', '0010_post_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='decription',
            new_name='description',
        ),
    ]
