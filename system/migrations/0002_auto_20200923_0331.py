# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-09-23 00:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='union',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='union',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
