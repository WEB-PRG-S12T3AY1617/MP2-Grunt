# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20170815_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='accept',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='reject',
            field=models.BooleanField(default=False),
        ),
    ]
