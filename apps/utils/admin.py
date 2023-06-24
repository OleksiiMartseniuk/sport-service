from django.contrib import admin

from .models import Event


class EventInline(admin.StackedInline):
    extra = 0
    verbose_name_plural = 'event'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'created',
    ]
    list_filter = ['created']
    search_fields = ['id']
    list_display_links = ['title']
    readonly_fields = ['created']
