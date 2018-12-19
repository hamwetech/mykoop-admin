# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-18 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'county',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='MessageTemplates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coop_share_purchase', models.TextField(blank=True, null=True)),
                ('member_share_purchase', models.TextField(blank=True, null=True)),
                ('member_registration', models.TextField(blank=True, null=True)),
                ('purchase_confirmation', models.TextField(blank=True, null=True)),
                ('payment_confirmation', models.TextField(blank=True, null=True)),
                ('supply_request', models.TextField(blank=True, null=True)),
                ('supply_confirmation', models.TextField(blank=True, null=True)),
                ('supply_cancelled', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'message_template',
            },
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'parish',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=50, verbose_name='Method')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'payment_method',
            },
        ),
        migrations.CreateModel(
            name='SubCounty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.County')),
            ],
            options={
                'db_table': 'sub_county',
            },
        ),
        migrations.CreateModel(
            name='SystemSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_message', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'system_settings',
            },
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('parish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.Parish')),
            ],
            options={
                'db_table': 'village',
            },
        ),
        migrations.AddField(
            model_name='parish',
            name='sub_county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty'),
        ),
        migrations.AddField(
            model_name='county',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.District'),
        ),
        migrations.AlterUniqueTogether(
            name='subcounty',
            unique_together=set([('county', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='parish',
            unique_together=set([('sub_county', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='county',
            unique_together=set([('district', 'name')]),
        ),
    ]
