# Generated by Django 4.2 on 2023-05-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0003_exercise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
