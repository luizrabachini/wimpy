from django.urls import path

from wimpy.events.api import EventAPIView

urlpatterns = [
    path(
        '',
        EventAPIView.as_view(),
        name='events'
    ),
]
