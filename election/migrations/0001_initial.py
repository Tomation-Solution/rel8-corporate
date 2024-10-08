# Generated by Django 3.2.13 on 2023-12-20 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BallotBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Election 1', max_length=300)),
                ('role_name', models.CharField(default='Role OF What?', max_length=300)),
                ('role_detail', models.TextField(default='')),
                ('is_close', models.BooleanField(default=False)),
                ('election_startDate', models.DateField(default=None, null=True)),
                ('election_endDate', models.DateField(default=None, null=True)),
                ('election_endTime', models.TimeField(default=None, null=True)),
                ('election_startTIme', models.TimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Postions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postion_name', models.CharField(max_length=90)),
                ('ballotbox', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='election.ballotbox')),
                ('members_that_has_cast_thier_vote', models.ManyToManyField(to='account.Memeber')),
            ],
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_vote', models.IntegerField()),
                ('youtubeVidLink', models.TextField()),
                ('aspirantBio', models.JSONField(default=None, null=True)),
                ('upload_manifesto_docs', models.FileField(default=None, null=True, upload_to='')),
                ('upload_manifesto_image', models.FileField(default=None, null=True, upload_to='')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.memeber')),
                ('postion', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='election.postions')),
            ],
        ),
    ]
