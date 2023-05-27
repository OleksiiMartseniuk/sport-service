from django.contrib import admin

from .models import WorkoutHistory


@admin.register(WorkoutHistory)
class AdminWorkoutHistory(admin.ModelAdmin):

    list_display = [
        'id',
        'user',
        'workout',
    ]
    list_filter = [
        'user',
        'workout',
        ('data_close', admin.EmptyFieldListFilter),
    ]
    readonly_fields = ['data_open']
