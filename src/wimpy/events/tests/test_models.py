from typing import Dict

import pytest
from django.db.utils import IntegrityError

from wimpy.events.constants import get_default_event_data_schema
from wimpy.events.models import Event, EventCategory, EventSchema, EventType


@pytest.mark.django_db
class TestEventCategory:

    def test_should_generate_slug_on_save(self):
        event_category: EventCategory = EventCategory(name='Some category')
        assert event_category.slug == ''
        assert str(event_category) == event_category.slug
        event_category.save()
        assert event_category.slug == 'some-category'
        assert str(event_category) == event_category.slug

    def test_should_override_slug_on_save(self, event_category):
        event_category.name = 'Name changed'
        event_category.save()
        assert event_category.slug == 'name-changed'

    def test_should_return_slug_in_str(self, event_category):
        assert str(event_category) == event_category.slug

    def test_should_keep_slug_unique(self, event_category):
        new_event_category: EventCategory = EventCategory(
            name=event_category.name,
            description='Different description',
        )
        with pytest.raises(IntegrityError):
            new_event_category.save()


@pytest.mark.django_db
class TestEventType:

    def test_should_generate_slug_on_save(self):
        event_type: EventType = EventType(name='Some type')
        assert event_type.slug == ''
        assert str(event_type) == event_type.slug
        event_type.save()
        assert event_type.slug == 'some-type'
        assert str(event_type) == event_type.slug

    def test_should_override_slug_on_save(self, event_type):
        event_type.name = 'Name changed'
        event_type.save()
        assert event_type.slug == 'name-changed'

    def test_should_return_slug_in_str(self, event_type):
        assert str(event_type) == event_type.slug

    def test_should_keep_slug_unique(self, event_type):
        new_event_type: EventType = EventType(
            name=event_type.name,
            description='Different description',
        )
        with pytest.raises(IntegrityError):
            new_event_type.save()


@pytest.mark.django_db
class TestEventSchema:

    def test_should_use_default_event_data_schema(
        self,
        event_category,
        event_type
    ):
        event_schema: EventSchema = EventSchema(
            category=event_category,
            type=event_type
        )
        assert event_schema.data_schema == get_default_event_data_schema()

    def test_should_use_custom_event_data_schema(
        self,
        event_category,
        event_type
    ):
        data_schema: Dict = {
            'type': 'object',
            'properties': {
                'number': {
                    'type': 'number'
                }
            }
        }
        event_schema: EventSchema = EventSchema(
            category=event_category,
            type=event_type,
            data_schema=data_schema,
        )
        assert event_schema.data_schema == data_schema

    def test_should_return_custom_str(self, event_schema):
        assert str(event_schema) == (
            f'{event_schema.category} - {event_schema.type}'
        )


@pytest.mark.django_db
class TestEvent:

    def test_should_return_dict_to_json(self, event: Event):
        assert event.to_json() == {
            'session_id': 'd2cff3b5-e16e-40f6-b97e-9c67013440ca',
            'category': 'some-category',
            'name': 'some-type',
            'data': {
                'host': 'localhost',
                'path': '/'
            },
            'timestamp': '2022-10-12 10:05:21.123456'
        }
