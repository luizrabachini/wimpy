import uuid

from rest_framework import serializers

from wimpy.constants import DEFAULT_DATETIME_FORMAT

__all__ = ['EventSerializer']


class EventSerializer(serializers.Serializer):

    event_id = serializers.UUIDField(default=str(uuid.uuid4()))
    session_id = serializers.UUIDField()
    category = serializers.SlugField(max_length=64)
    name = serializers.SlugField(max_length=64)
    data = serializers.DictField()
    timestamp = serializers.DateTimeField(format=DEFAULT_DATETIME_FORMAT)
