# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-03 01:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0002_auto_20200923_0331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='MemberOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(blank=True, max_length=255)),
                ('order_reference', models.CharField(blank=True, max_length=255)),
                ('order_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20)),
                ('status', models.CharField(default='PENDING', max_length=255)),
                ('order_date', models.DateTimeField()),
                ('accept_date', models.DateTimeField(blank=True, null=True)),
                ('reject_date', models.DateTimeField(blank=True, null=True)),
                ('reject_reason', models.CharField(blank=True, max_length=120, null=True)),
                ('ship_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_accept_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_reject_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_reject_reason', models.CharField(blank=True, max_length=120, null=True)),
                ('collect_date', models.DateTimeField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('union', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Union')),
            ],
            options={
                'db_table': 'member_order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Item')),
                ('order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='supplier.MemberOrder')),
            ],
            options={
                'db_table': 'order_item',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('union', models.ManyToManyField(to='system.Union')),
            ],
            options={
                'db_table': 'supplier',
            },
        ),
        migrations.CreateModel(
            name='SupplierUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_user',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier'),
        ),
    ]
