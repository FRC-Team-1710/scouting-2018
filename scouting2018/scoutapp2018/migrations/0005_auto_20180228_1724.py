# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoutapp2018', '0004_auto'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='match',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auto',
            name='team',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]