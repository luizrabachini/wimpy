import uuid
from typing import Dict

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


@pytest.fixture
def valid_event_data(event_type) -> Dict:
    return {
        'application_id': 'test',
        'session_id': str(uuid.uuid4()),
        'category': event_type.category.slug,
        'name': event_type.slug,
        'data': {
            'some': 'data'
        },
        'timestamp': '2022-10-12 10:05:21.123456',
    }
