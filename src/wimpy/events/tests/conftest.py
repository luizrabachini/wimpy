import pytest

from wimpy.events.models import EventCategory, EventType


@pytest.fixture
def event_category() -> EventCategory:
    event_category: EventCategory = EventCategory(
        name='Some category',
        description='Some category description',
    )
    event_category.save()
    return event_category


@pytest.fixture
def event_type(event_category) -> EventType:
    event_type: EventType = EventType(
        category=event_category,
        name='Some type',
        description='Some type description',
    )
    event_type.save()
    return event_type
