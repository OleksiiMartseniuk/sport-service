# Generated by Django 4.2 on 2023-06-17 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_exercisehistory_close_data_exercisehistory_open_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercisehistory',
            old_name='close_data',
            new_name='close_date',
        ),
        migrations.RenameField(
            model_name='exercisehistory',
            old_name='open_data',
            new_name='open_date',
        ),
    ]
