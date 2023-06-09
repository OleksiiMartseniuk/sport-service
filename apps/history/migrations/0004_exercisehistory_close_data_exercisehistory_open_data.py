# Generated by Django 4.2 on 2023-06-17 06:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0003_exercisehistory_exerciseapproaches'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisehistory',
            name='close_data',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='exercisehistory',
            name='open_data',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
    ]
