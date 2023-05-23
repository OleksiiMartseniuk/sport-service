# Generated by Django 4.2 on 2023-05-23 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workout', '0005_alter_exercise_day'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutHistory',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('detail_info', models.JSONField(default=list)),
                ('data_open', models.DateTimeField(auto_now_add=True)),
                (
                    'data_close',
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='history_workout',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'workout',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='history_workout',
                        to='workout.workout',
                        ),
                    ),
            ],
        ),
    ]
