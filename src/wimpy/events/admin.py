from django.contrib import admin

from wimpy.events.models import Event, EventCategory, EventSchema, EventType


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')


@admin.register(EventSchema)
class EventSchemaAdmin(admin.ModelAdmin):

    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = ('session_id', 'category', 'name', 'timestamp')
