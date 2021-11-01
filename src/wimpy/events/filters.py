from django_filters import rest_framework as filters

from wimpy.events.models import Event

__all__ = ['EventFilter']


class EventFilter(filters.FilterSet):

    min_timestamp = filters.NumberFilter(
        field_name='timestamp',
        lookup_expr='gte'
    )
    max_timestamp = filters.NumberFilter(
        field_name='timestamp',
        lookup_expr='lte'
    )

    class Meta:
        model = Event
        fields = [
            'session_id',
            'category',
            'name',
            'min_timestamp',
            'max_timestamp',
        ]
