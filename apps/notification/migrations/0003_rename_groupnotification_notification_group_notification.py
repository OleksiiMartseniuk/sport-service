# Generated by Django 4.2 on 2023-04-29 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notification_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='GroupNotification',
            new_name='group_notification',
        ),
    ]