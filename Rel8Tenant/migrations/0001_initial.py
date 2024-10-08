# Generated by Django 3.2.13 on 2023-12-20 14:34

from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0015_edit_solarschedule_events_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('timezone', timezone_field.fields.TimeZoneField(default='UTC')),
                ('name', models.CharField(max_length=100)),
                ('paystack_publickey', models.TextField(default='null')),
                ('paystack_secret', models.TextField(default='null')),
                ('flutterwave_publickey', models.TextField(default='null')),
                ('flutterwave_secret', models.TextField(default='null')),
                ('paid_until', models.DateTimeField()),
                ('on_trial', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.EmailField(max_length=254)),
                ('payment_plan', models.CharField(choices=[('individual', 'Individual'), ('organization', 'Organization')], default='individual', max_length=25)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Financial_and_nonFinancialMembersRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(null=True, upload_to='financial_and_nonfinancialmembersrecord/%d%m/')),
                ('name', models.CharField(default='', max_length=400)),
                ('for_financial', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodicTaskTenantLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_tenant_timezone', models.BooleanField(default=False)),
                ('periodic_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_task_tenant_link', to='django_celery_beat.periodictask')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_task_tenant_links', to='Rel8Tenant.client')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='Rel8Tenant.client')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
