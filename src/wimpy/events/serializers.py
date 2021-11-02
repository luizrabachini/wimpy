import logging
import uuid
from typing import Dict

from django.conf import settings
from django.core.cache import caches
from jsonschema import ValidationError, validate
from kafka import KafkaProducer
from rest_framework import serializers

from wimpy.helpers.data import serialize_data
from wimpy.events.models import Event, EventCategory, EventSchema, EventType

__all__ = ['EventSerializer']

logger = logging.getLogger(__name__)

cache = caches['default']


class EventSerializer(serializers.ModelSerializer):

    idempotency_key: serializers.UUIDField = serializers.UUIDField(
        default=str(uuid.uuid4())
    )

    category: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=EventCategory.objects.all(),
    )
    name: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=EventType.objects.all(),
    )

    _broker: Dict = {
        'kafka_producer': None
    }

    class Meta:
        model = Event
        exclude = ('id',)

    @classmethod
    def reset(cls):
        cls._broker['kafka_producer'] = None

    @property
    def kafka_producer(self) -> KafkaProducer:
        if not self._broker['kafka_producer']:
            logger.info(
                'Connecting to Kafka '
                f'Servers {settings.KAFKA_BOOTSTRAP_SERVERS}'
            )
            self._broker['kafka_producer'] = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=serialize_data,
            )
            logger.info('Connected with Kafka Servers')
        return self._broker['kafka_producer']

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

    def create(self, validated_data) -> Event:
        idempotency_key: str = validated_data.pop('idempotency_key')
        event = Event(**validated_data)

        if settings.ASYNC_EVENTS_ENABLED:
            try:
                data: Dict = event.to_json()
                logger.info(
                    f'Sending data {data} to '
                    f'topic {settings.ASYNC_EVENTS_TOPIC}'
                )
                result = self.kafka_producer.send(
                    settings.ASYNC_EVENTS_TOPIC,
                    data
                )
                logger.info(f'Data sent with result {result}')
            except Exception:
                logger.exception('Unknown error on publish data {data}')
                raise

            return event

        event.save()

        return event
