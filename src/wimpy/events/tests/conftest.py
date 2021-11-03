import uuid
from datetime import datetime
from typing import Dict
from unittest import mock

import pytest

from wimpy.constants import DEFAULT_DATETIME_FORMAT
from wimpy.events.models import Event, EventCategory, EventSchema, EventType
from wimpy.events.serializers import EventSerializer


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
def event(event_schema: EventSchema):
    return Event(
        session_id='d2cff3b5-e16e-40f6-b97e-9c67013440ca',
        category=event_schema.category,
        name=event_schema.type,
        data={
            'host': 'localhost',
            'path': '/',
        },
        timestamp=datetime.strptime(
            '2022-10-12 10:05:21.123456',
            DEFAULT_DATETIME_FORMAT,
        ),
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


@pytest.fixture(autouse=True)
def reset_event_serializer():
    EventSerializer.reset()


@pytest.fixture
def consumer_sleep_mock() -> mock.Mock:
    with mock.patch(
        'wimpy.events.consumers.sleep'
    ) as sleep_mock:
        yield sleep_mock


@pytest.fixture
def consumer_kafka_mock() -> mock.Mock:
    with mock.patch(
        'wimpy.events.consumers.EventConsumer.kafka_consumer'
    ) as kafka_mock:
        yield kafka_mock


@pytest.fixture
def consumer_stopped_mock() -> mock.Mock:
    with mock.patch(
        'wimpy.events.consumers.EventConsumer.stopped',
        new_callable=mock.PropertyMock
    ) as stopped_mock:
        yield stopped_mock


@pytest.fixture
def consumer_process_mock() -> mock.Mock:
    with mock.patch(
        'wimpy.events.consumers.EventConsumer._process'
    ) as process_mock:
        yield process_mock
