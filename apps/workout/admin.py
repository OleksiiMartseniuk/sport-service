from django.contrib import admin

from .models import Category, Workout, Exercise


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'publish',
        'created',
    )
    list_filter = (
        'publish',
        'user',
        'created',
    )
    search_fields = (
        'id',
        'title',
    )


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'workout',
        'publish',
        'day',
        'created',
    )
    list_filter = (
        'workout__title',
        'publish',
        'day',
        'created',
    )
    search_fields = (
        'title',
        'id',
    )
