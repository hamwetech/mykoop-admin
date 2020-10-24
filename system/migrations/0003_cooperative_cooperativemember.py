# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-10-03 01:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0002_systemsettings_mobile_money_payment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0002_auto_20200923_0331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='cooperatives/')),
                ('code', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('contact_person_name', models.CharField(max_length=150)),
                ('contribution_total', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('shares', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('is_active', models.BooleanField(default=0)),
                ('send_message', models.BooleanField(default=0, help_text="If not set, the cooperative member will not receive SMS's when sent.")),
                ('date_joined', models.DateField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District')),
                ('sub_county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty')),
            ],
            options={
                'db_table': 'cooperative',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='member/')),
                ('member_id', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('title', models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Miss', 'Miss'), ('Mrs', 'Mrs'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Hon', 'Hon')], max_length=25, null=True)),
                ('surname', models.CharField(max_length=150)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('other_name', models.CharField(blank=True, max_length=150, null=True)),
                ('is_refugee', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('maritual_status', models.CharField(blank=True, choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widow'), ('Divorced', 'Divorced')], max_length=10, null=True)),
                ('id_number', models.CharField(blank=True, max_length=150, null=True)),
                ('id_type', models.CharField(blank=True, choices=[('nin', 'National ID'), ('dl', 'Drivers Lisence'), ('pp', 'PassPort'), ('o', 'Other')], max_length=150, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('other_phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('village', models.CharField(blank=True, max_length=150, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('gps_coodinates', models.CharField(blank=True, max_length=150, null=True)),
                ('coop_role', models.CharField(choices=[('Chairperson', 'Chairperson'), ('Vice', 'Vice'), ('Treasurer', 'Treasurer'), ('Secretary', 'Secretary'), ('Committee Member', 'Committee Member'), ('Member', 'Member')], max_length=150)),
                ('cotton_acreage', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('soya_beans_acreage', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('soghum_acreage', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('land_acreage', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('product', models.CharField(blank=True, max_length=255, null=True)),
                ('shares', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('share_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('collection_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32)),
                ('collection_quantity', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=32)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=1)),
                ('qrcode', models.ImageField(blank=True, null=True, upload_to='qrcode')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Cooperative')),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.County')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District')),
                ('parish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.Parish')),
                ('sub_county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty')),
            ],
            options={
                'db_table': 'cooperative_member',
            },
        ),
    ]