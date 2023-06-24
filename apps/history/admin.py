from django.contrib import admin

from apps.utils.admin import EventInline

from .models import WorkoutHistory, ExerciseHistory, ExerciseApproaches


class EventWorkoutHistoryInline(EventInline):
    model = WorkoutHistory.event.through


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
        ('close_date', admin.EmptyFieldListFilter),
    ]
    readonly_fields = ['open_date']
    exclude = ['event']
    inlines = [EventWorkoutHistoryInline]


class EventExerciseHistoryInline(EventInline):
    model = ExerciseHistory.event.through


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
        EventExerciseHistoryInline,
        ExerciseApproachesInline,
    ]
