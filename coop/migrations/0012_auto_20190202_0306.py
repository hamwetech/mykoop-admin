# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-02 00:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coop', '0011_auto_20190202_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='is_member',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='collection',
            name='non_member',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
    ]
