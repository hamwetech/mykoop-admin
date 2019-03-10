# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-04 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0001_initial'),
        ('coop', '0003_cooperativemember_share_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='cooperativemember',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.County'),
        ),
    ]