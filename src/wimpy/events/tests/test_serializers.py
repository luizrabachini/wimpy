from typing import Dict
from unittest import mock

import pytest
from django.conf import settings

from wimpy.events.models import EventCategory, EventSchema, EventType
from wimpy.events.serializers import EventSerializer


@pytest.mark.django_db
class TestEventSerializer:

    def test_get_data_schema(self, event_schema: EventSchema):
        data_schema: Dict = EventSerializer.get_data_schema(
            category=event_schema.category,
            type=event_schema.type
        )
        assert data_schema == event_schema.data_schema

    def test_get_data_schema_should_cache(self, event_schema: EventSchema):
        with mock.patch('wimpy.events.serializers.cache') as cache_mock:
            EventSerializer.get_data_schema(
                category=event_schema.category,
                type=event_schema.type
            )
            assert cache_mock.get.called_once_with(
                f'{event_schema.category}-{event_schema.type}'
            )
            assert cache_mock.set.called_once_with(
                f'{event_schema.category}-{event_schema.type}',
                event_schema.data_schema,
                settings.EVENT_DATA_SCHEMA_CACHE_TTL
            )

    def test_get_data_schema_should_return_from_cache(
        self,
        event_schema: EventSchema
    ):
        cached_data_schema: Dict = {'some': 'data'}
        with mock.patch('wimpy.events.serializers.cache') as cache_mock:
            cache_mock.get.return_value = cached_data_schema
            with mock.patch(
                'wimpy.events.serializers.EventSchema.objects.get'
            ) as mock_objects:
                data_schema: Dict = EventSerializer.get_data_schema(
                    category=event_schema.category,
                    type=event_schema.type
                )
                assert data_schema == cached_data_schema
                assert not cache_mock.set.called
                assert not mock_objects.called

    def test_get_data_schema_should_continue_on_cache_get_error(
        self,
        caplog,
        event_schema: EventSchema
    ):
        with mock.patch('wimpy.events.serializers.cache') as cache_mock:
            cache_mock.get.side_effect = Exception('Ploft!')
            data_schema: Dict = EventSerializer.get_data_schema(
                category=event_schema.category,
                type=event_schema.type
            )
            assert data_schema == event_schema.data_schema
            assert cache_mock.set.called
            assert 'Error on get data schema from cache' in caplog.text

    def test_get_data_schema_should_continue_on_cache_set_error(
        self,
        caplog,
        event_schema: EventSchema
    ):
        with mock.patch('wimpy.events.serializers.cache') as cache_mock:
            cache_mock.get.return_value = None
            cache_mock.set.side_effect = Exception('Ploft!')
            data_schema: Dict = EventSerializer.get_data_schema(
                category=event_schema.category,
                type=event_schema.type
            )
            assert data_schema == event_schema.data_schema
            assert cache_mock.get.called
            assert 'Error on set data schema in cache' in caplog.text

    def test_validate_event(self, valid_event_data: Dict):
        serializer: EventSerializer = EventSerializer(data=valid_event_data)
        assert serializer.is_valid()

    def test_validate_event_with_invalid_data(
        self,
        caplog,
        valid_event_data: Dict
    ):
        valid_event_data['data'] = {
            'host': 'localhost',
        }
        serializer: EventSerializer = EventSerializer(data=valid_event_data)
        assert not serializer.is_valid()
        assert 'Invalid schema found' in caplog.text

    def test_validate_event_with_invalid_category(
        self,
        caplog,
        valid_event_data: Dict
    ):
        event_category: EventCategory = EventCategory(name='Some new category')
        event_category.save()
        valid_event_data['category'] = event_category.slug
        serializer: EventSerializer = EventSerializer(data=valid_event_data)
        assert not serializer.is_valid()
        assert 'Event schema not found' in caplog.text

    def test_validate_event_with_invalid_type(
        self,
        caplog,
        valid_event_data: Dict
    ):
        event_type: EventType = EventType(name='Some new type')
        event_type.save()
        valid_event_data['name'] = event_type.slug
        serializer: EventSerializer = EventSerializer(data=valid_event_data)
        assert not serializer.is_valid()
        assert 'Event schema not found' in caplog.text
