# Generated by Django 3.2.13 on 2023-12-20 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
        ('Dueapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='due_user',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='due',
            name='chapters',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.chapters'),
        ),
        migrations.AddField(
            model_name='due',
            name='dues_for_membership_grade',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.membershipgrade'),
        ),
        migrations.AddField(
            model_name='due',
            name='exco',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.excorole'),
        ),
        migrations.AddField(
            model_name='deactivatingdue_user',
            name='deactivatingdue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dueapp.deactivatingdue'),
        ),
        migrations.AddField(
            model_name='deactivatingdue_user',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deactivatingdue',
            name='chapters',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.chapters'),
        ),
    ]
