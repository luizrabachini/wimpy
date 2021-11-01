import logging
from typing import Dict

from django.conf import settings
from django.core.cache import caches
from jsonschema import ValidationError, validate
from rest_framework import serializers

from wimpy.events.models import Event, EventCategory, EventSchema, EventType

__all__ = ['EventSerializer']

logger = logging.getLogger(__name__)

cache = caches['default']


class EventSerializer(serializers.ModelSerializer):

    category: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=EventCategory.objects.all(),
    )
    name: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=EventType.objects.all(),
    )

    class Meta:
        model = Event
        exclude = ('id',)

    @classmethod
    def get_data_schema(
        cls,
        category: EventCategory,
        type: EventType
    ) -> Dict:
        cache_key: str = f'{category}-{type}'
        data_schema: Dict = None

        try:
            data_schema: Dict = cache.get(cache_key)
        except Exception:
            logger.exception('Error on get data schema from cache')

        if not data_schema:
            schema: EventSchema = EventSchema.objects.get(
                category=category,
                type=type,
            )
            data_schema = schema.data_schema

            try:
                cache.set(
                    cache_key,
                    data_schema,
                    settings.EVENT_DATA_SCHEMA_CACHE_TTL
                )
            except Exception:
                logger.exception('Error on set data schema in cache')

        logger.debug(
            f'Found schema {data_schema} for '
            f'category {category} and {type}'
        )

        return data_schema

    def validate(self, data: Dict):
        try:
            data_schema: Dict = self.get_data_schema(
                category=data['category'],
                type=data['name']
            )
            validate(data['data'], data_schema)
        except ValidationError:
            logger.warn(
                f'Invalid schema found in {data["session_id"]}. '
                f'Data: {data["data"]}. '
                f'Schema: {data_schema}.'
            )
            raise serializers.ValidationError('Invalid data')
        except EventSchema.DoesNotExist:
            logger.critical(
                'Event schema not found for '
                f'category {data["category"]} '
                f'and type {data["name"]}.'
            )
            raise serializers.ValidationError('Data schema not found')

        return data
