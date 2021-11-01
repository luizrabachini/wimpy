import uuid
from typing import Dict

import pytest

from wimpy.events.models import Event, EventCategory, EventSchema, EventType


@pytest.fixture
def event_category() -> EventCategory:
    event_category: EventCategory = EventCategory(
        name='Some category',
        description='Some category description',
    )
    event_category.save()
    return event_category


@pytest.fixture
def event_type() -> EventType:
    event_type: EventType = EventType(
        name='Some type',
        description='Some type description',
    )
    event_type.save()
    return event_type


@pytest.fixture
def event_schema(
    event_category: EventCategory,
    event_type: EventType
) -> EventSchema:
    event_schema: EventSchema = EventSchema(
        category=event_category,
        type=event_type,
    )
    event_schema.save()
    return event_schema


@pytest.fixture
def event(event_schema):
    return Event(
        session_id='d2cff3b5-e16e-40f6-b97e-9c67013440ca',
        category=event_schema.category,
        name=event_schema.type,
        data={
            'host': 'localhost',
            'path': '/',
        },
        timestamp='2022-10-12 10:05:21.123456',
    )


@pytest.fixture
def valid_event_data(event_schema) -> Dict:
    return {
        'session_id': str(uuid.uuid4()),
        'category': event_schema.category.slug,
        'name': event_schema.type.slug,
        'data': {
            'host': 'localhost',
            'path': '/',
        },
        'timestamp': '2022-10-12 10:05:21.123456',
    }
