# Generated by Django 3.2.13 on 2023-12-20 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Rel8Tenant', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid_succesfully', models.BooleanField(default=False)),
                ('paystack_key', models.CharField(max_length=100)),
                ('is_end', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rel8Tenant.client')),
            ],
        ),
        migrations.CreateModel(
            name='IndividualSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paystack_key', models.CharField(max_length=100)),
                ('is_end', models.BooleanField(default=False)),
                ('is_paid_succesfully', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.memeber')),
            ],
        ),
    ]
