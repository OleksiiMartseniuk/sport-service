from django.contrib import admin

from .models import Category, Workout


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
    search_fields = ('title',)
