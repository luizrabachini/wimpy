from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from wimpy.events.filters import EventFilter
from wimpy.events.models import Event
from wimpy.events.serializers import EventSerializer

__all__ = ['EventAPIView']


class EventAPIView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
