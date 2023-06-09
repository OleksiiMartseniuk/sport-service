# Generated by Django 4.2 on 2023-06-03 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0005_alter_exercise_day'),
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workouthistory',
            name='workout',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='history_workout',
                to='workout.workout',
            ),
        ),
    ]
