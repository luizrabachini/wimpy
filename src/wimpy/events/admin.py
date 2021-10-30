from django.contrib import admin

from wimpy.events.models import EventCategory, EventType


@admin.register(EventCategory)
class EventCategorydmin(admin.ModelAdmin):

    list_display = ('name', 'slug')


@admin.register(EventType)
class EventTypedmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
