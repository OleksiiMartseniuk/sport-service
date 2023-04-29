from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = [
        'subject',
        'status',
        'group_notification',
        'created',
    ]
    list_filter = [
        'status',
        'group_notification',
        'user',
    ]
