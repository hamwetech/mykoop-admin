# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-18 18:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalIdentification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=50, verbose_name='Method')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'animal_identification',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_date', models.DateTimeField()),
                ('collection_reference', models.CharField(blank=True, max_length=255)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collection',
            },
        ),
        migrations.CreateModel(
            name='CommonDisease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('local', models.CharField(blank=True, max_length=160, null=True, verbose_name='Local Name')),
                ('description', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'common_diseases',
            },
        ),
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
                ('product', models.ManyToManyField(blank=True, to='product.Product')),
                ('sub_county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty')),
            ],
            options={
                'db_table': 'cooperative',
            },
        ),
        migrations.CreateModel(
            name='CooperativeAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cooperative_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cooperative_admin',
            },
        ),
        migrations.CreateModel(
            name='CooperativeContribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('new_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('indicator', models.CharField(max_length=120)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='cooperatives/files/')),
                ('remark', models.CharField(blank=True, max_length=120, null=True)),
                ('transaction_date', models.DateTimeField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.PaymentMethod')),
            ],
            options={
                'db_table': 'cooperative_contribution',
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
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('maritual_status', models.CharField(blank=True, choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widow'), ('Divorced', 'Divorced')], max_length=10, null=True)),
                ('id_number', models.CharField(blank=True, max_length=150, null=True)),
                ('id_type', models.CharField(blank=True, choices=[('nin', 'National ID'), ('dl', 'Drivers Lisence'), ('pp', 'PassPort'), ('o', 'Other')], max_length=150, null=True)),
                ('phone_number', models.CharField(max_length=12, null=True, unique=True)),
                ('other_phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('gps_coodinates', models.CharField(blank=True, max_length=150, null=True)),
                ('coop_role', models.CharField(choices=[('Chairman', 'Chairman'), ('Vice Chairman', 'Vice Chairman'), ('Treasurer', 'Treasurer'), ('Secretary', 'Secretary'), ('Member', 'Member'), ('Secretary Manager', 'Secretary Manager'), ('Patron', 'Patron')], max_length=150)),
                ('cotton_trees', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='No of Cotton Trees')),
                ('collection_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_active', models.BooleanField(default=1)),
                ('qrcode', models.ImageField(blank=True, null=True, upload_to='qrcode')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative')),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District')),
                ('sub_county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty')),
                ('village', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.Parish')),
            ],
            options={
                'db_table': 'cooperative_member',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberBusiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='Farm Name')),
                ('gps_coodinates', models.CharField(blank=True, help_text='Seperate Longinture and Latitude values with a comma(,). Longitude values come first.', max_length=150, null=True)),
                ('size', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Size of Farm')),
                ('size_units', models.CharField(blank=True, choices=[('acre', 'Acres'), ('ha', 'Hectare'), ('sq_m', 'Square Meters'), ('sq_km', 'Square Kilometers')], max_length=150, null=True)),
                ('fenced', models.BooleanField(default=0)),
                ('paddock', models.BooleanField(default=0)),
                ('water_source', models.CharField(blank=True, choices=[('Dam', 'Dam'), ('Spring', 'Spring'), ('Rain', 'Rain'), ('Swamp', 'Swamp')], max_length=12, null=True)),
                ('animal_identification', models.CharField(blank=True, max_length=12, null=True)),
                ('other_animal_diseases', models.TextField(blank=True, null=True, verbose_name='Other Common Disease Specify')),
                ('tick_control', models.CharField(blank=True, max_length=12, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('common_diseases', models.ManyToManyField(blank=True, to='coop.CommonDisease')),
                ('cooperative_member', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
                ('farm_district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District')),
                ('farm_sub_county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty')),
            ],
            options={
                'db_table': 'cooperative_member_business',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberHerdFemale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_adults', models.PositiveIntegerField(blank=True, default=0, verbose_name='Adults')),
                ('heifers', models.PositiveIntegerField(blank=True, default=0)),
                ('f_calves', models.PositiveIntegerField(blank=True, default=0, verbose_name='Calves')),
                ('f_total', models.PositiveIntegerField(blank=True, default=0, verbose_name='Total')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'herd_female',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberHerdMale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adults', models.PositiveIntegerField(blank=True, default=0)),
                ('bullocks', models.PositiveIntegerField(blank=True, default=0)),
                ('calves', models.PositiveIntegerField(blank=True, default=0)),
                ('total', models.PositiveIntegerField(blank=True, default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'herd_male',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=12)),
                ('animal_type', models.CharField(choices=[('Adult', 'Adults'), ('Bullock', 'Bullocks'), ('Calf', 'Calfs')], max_length=12)),
                ('quantity', models.PositiveIntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductVariation')),
            ],
            options={
                'db_table': 'cooperative_member_product',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberProductDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
                ('product_variation', models.ManyToManyField(blank=True, to='product.ProductVariation')),
            ],
            options={
                'db_table': 'cooperative_member_product_definition',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberProductQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('adult', models.PositiveIntegerField(blank=True, default=0)),
                ('heifer', models.PositiveIntegerField(blank=True, default=0)),
                ('bullock', models.PositiveIntegerField(blank=True, default=0)),
                ('calves', models.PositiveIntegerField(blank=True, default=0)),
                ('total', models.PositiveIntegerField(blank=True, default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'cooperative_member_product_quantity',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberSharesLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=254, null=True)),
                ('shares_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shares', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_shares', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('transaction_date', models.DateTimeField()),
                ('remark', models.CharField(blank=True, max_length=160, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.PaymentMethod')),
            ],
            options={
                'db_table': 'cooperative_member_shares_log',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberSubscriptionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=254, null=True)),
                ('year', models.PositiveIntegerField()),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField()),
                ('remark', models.CharField(blank=True, max_length=160, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('received_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'cooperative_member_subscription_log',
            },
        ),
        migrations.CreateModel(
            name='CooperativeMemberSupply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nearest_market', models.CharField(blank=True, max_length=150, null=True)),
                ('product_average_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Estimate Cost per Animal')),
                ('price_per_kilo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Estimate cost Per Kilo')),
                ('probable_sell_month', models.CharField(blank=True, max_length=250, null=True)),
                ('sell_to_cooperative_society', models.BooleanField(default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'cooperative_member_supply',
            },
        ),
        migrations.CreateModel(
            name='CooperativeSharePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current', models.BooleanField(default=0)),
                ('remark', models.CharField(max_length=120)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cooperative_share_price',
            },
        ),
        migrations.CreateModel(
            name='CooperativeShareTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=254, null=True)),
                ('share_value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=20)),
                ('shares_bought', models.DecimalField(decimal_places=2, max_digits=20)),
                ('new_shares', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('transaction_date', models.DateTimeField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.PaymentMethod')),
            ],
            options={
                'db_table': 'cooperative_share_transaction',
            },
        ),
        migrations.CreateModel(
            name='CooperativeTrainingModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=150)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'cooperative_training_module',
            },
        ),
        migrations.CreateModel(
            name='DewormingSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deworm_date', models.DateField(blank=True, null=True)),
                ('dewormer', models.CharField(blank=True, max_length=128, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('cooperative_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'deworming_schedule',
            },
        ),
        migrations.CreateModel(
            name='MemberSupplyRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_reference', models.CharField(blank=True, max_length=254, null=True)),
                ('supply_date', models.DateField()),
                ('status', models.CharField(blank=True, choices=[('PENDING', 'PENDING'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=15)),
                ('confirmed_by', models.CharField(blank=True, max_length=120, null=True)),
                ('comfirmation_method', models.CharField(blank=True, max_length=120, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('confirmation_logged_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirmer', to=settings.AUTH_USER_MODEL)),
                ('cooperative_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cooperative_member_supply_request',
            },
        ),
        migrations.CreateModel(
            name='MemberSupplyRequestVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('breed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.ProductVariation')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('supply_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.MemberSupplyRequest')),
            ],
            options={
                'db_table': 'member_supply_request_variation',
            },
        ),
        migrations.CreateModel(
            name='MemberSupplySchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'cooperative_member_supply_schedule',
            },
        ),
        migrations.CreateModel(
            name='MemberTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=16)),
                ('transaction_reference', models.CharField(max_length=120)),
                ('entry_type', models.CharField(max_length=120)),
                ('balance_before', models.DecimalField(decimal_places=2, max_digits=9)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('balance_after', models.DecimalField(decimal_places=2, max_digits=9)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember')),
            ],
            options={
                'db_table': 'member_transaction',
            },
        ),
        migrations.CreateModel(
            name='TickControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=50, verbose_name='Method')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tick_control',
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='collection',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductVariation'),
        ),
        migrations.AlterUniqueTogether(
            name='cooperativeshareprice',
            unique_together=set([('price', 'current')]),
        ),
        migrations.AlterUniqueTogether(
            name='cooperativemembersubscriptionlog',
            unique_together=set([('cooperative_member', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='cooperativememberproduct',
            unique_together=set([('cooperative_member', 'product_variation', 'gender', 'animal_type')]),
        ),
    ]
