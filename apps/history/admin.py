from django.contrib import admin

from .models import WorkoutHistory, ExerciseHistory, ExerciseApproaches


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


class EventInline(admin.StackedInline):
    model = ExerciseHistory.event.through
    extra = 0
    verbose_name_plural = 'event'


class ExerciseApproachesInline(admin.StackedInline):
    model = ExerciseApproaches
    extra = 0


@admin.register(ExerciseHistory)
class AdminExerciseHistory(admin.ModelAdmin):

    list_display = [
        'id',
        'exercises_title',
        'workout_title',
    ]
    list_filter = [
        'exercises',
        'history_workout',
    ]
    exclude = ['event']
    readonly_fields = ['open_date']
    inlines = [
        EventInline,
        ExerciseApproachesInline,
    ]
