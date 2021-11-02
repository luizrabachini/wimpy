import logging
import signal
from time import sleep
from typing import Dict

from django.conf import settings
from kafka import KafkaConsumer

from wimpy.events.models import Event, EventCategory, EventType
from wimpy.helpers.data import deserialize_data

__all__ = ['EventConsumer']

logger = logging.getLogger(__name__)


class EventConsumer:

    _stopped: bool = False
    _kafka_consumer: KafkaConsumer = None

    def __init__(self, *args, **kwargs):
        super(EventConsumer, self).__init__(*args, **kwargs)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    @property
    def stopped(self) -> bool:
        return self._stopped

    @property
    def kafka_consumer(self) -> KafkaConsumer:
        if not self._kafka_consumer:
            logger.info(
                'Connecting to Kafka '
                f'Servers {settings.KAFKA_BOOTSTRAP_SERVERS}'
            )
            self._kafka_consumer = KafkaConsumer(
                settings.ASYNC_EVENTS_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                client_id=settings.KAFKA_CONSUMER_CLIENT_ID,
                group_id=settings.KAFKA_CONSUMER_GROUP_ID,
                enable_auto_commit=settings.KAFKA_CONSUMER_AUTO_COMMIT,
                auto_offset_reset=settings.KAFKA_CONSUMER_OFFSET_RESET,
                max_poll_records=settings.KAFKA_CONSUMER_MAX_POLL_RECORDS,
                max_poll_interval_ms=settings.KAFKA_CONSUMER_MAX_POOL_INTERVAL,
                value_deserializer=deserialize_data
            )
            logger.info('Connected with Kafka Servers')
        return self._kafka_consumer

    def _process(self, message: Dict):
        event_category: EventCategory = EventCategory.objects.get(
            slug=message.pop('category')
        )
        event_type: EventType = EventType.objects.get(
            slug=message.pop('name')
        )
        event: Event = Event(
            category=event_category,
            name=event_type,
            **message
        )
        event.save()
        logger.debug(f'Event {event} created for message {message}')

    def start(self):
        while not self.stopped:
            messages_pack = self.kafka_consumer.poll()
            for _, messages in messages_pack.items():
                for message in messages:
                    logger.debug(f'Processing message {message}')
                    self._process(message=message.value)
            sleep(1)

    def stop(self, *args, **kwargs):
        logger.info('Stopping consumer')
        self._stopped = True
