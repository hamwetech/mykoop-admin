# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-23 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coop', '0002_orderitem_unit_price'),
        ('activity', '0006_auto_20190222_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsession',
            name='cooperative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='coop_member',
            field=models.ManyToManyField(blank=True, to='coop.CooperativeMember'),
        ),
    ]