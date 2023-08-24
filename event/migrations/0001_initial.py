# Generated by Django 3.2.13 on 2023-08-23 20:15

import cloudinary_storage.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=355)),
                ('is_paid_event', models.BooleanField(default=False)),
                ('re_occuring', models.BooleanField(default=False)),
                ('is_virtual', models.BooleanField(default=False)),
                ('event_docs', models.FileField(default=None, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='meeting_docs/%d/')),
                ('is_for_excos', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=4, default=0.0, max_digits=19)),
                ('is_active', models.BooleanField(default=False)),
                ('image', models.ImageField(default=None, null=True, upload_to='events/image/')),
                ('address', models.TextField(default=' ')),
                ('organiser_name', models.CharField(blank=True, default='', max_length=200)),
                ('organiser_extra_info', models.CharField(blank=True, default='', max_length=200)),
                ('organiserImage', models.ImageField(default=None, null=True, upload_to='event_organiser/%d/')),
                ('event_extra_details', models.TextField(blank=True, default='')),
                ('startDate', models.DateField(blank=True, null=True)),
                ('startTime', models.TimeField(blank=True, null=True)),
                ('scheduletype', models.CharField(choices=[('day_of_week', 'Day Of Week'), ('month_of_year', 'Month Of Year'), ('day_of_month', 'Day Of Month'), ('day_of_week_and_month_of_year', 'Day Of Week And Month Of Year'), ('day_of_month_and_month_of_year', 'Day Of Month And Month Of Year')], default='day_of_week', max_length=200)),
                ('schedule', models.JSONField(null=True)),
                ('chapters', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.chapters')),
                ('commitee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.commiteegroup')),
                ('exco', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.excorole')),
            ],
        ),
        migrations.CreateModel(
            name='EventDue_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paystack_key', models.TextField(default='')),
                ('is_paid', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RescheduleEventRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(blank=True, null=True)),
                ('startTime', models.TimeField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventProxyAttendies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participants', models.JSONField(default=dict)),
                ('event_due_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.eventdue_user')),
            ],
        ),
    ]
