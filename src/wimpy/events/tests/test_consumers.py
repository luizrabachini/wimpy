import copy
import signal
from typing import Dict
from unittest import mock

import pytest
from django.conf import settings

from wimpy.events.consumers import EventConsumer
from wimpy.events.models import Event
from wimpy.helpers.data import deserialize_data


@pytest.mark.django_db
class TestEventConsumer:

    def test_should_register_signals(self):
        with mock.patch(
            'wimpy.events.consumers.signal'
        ) as signal_mock:
            consumer: EventConsumer = EventConsumer()
            assert signal_mock.signal.called_once_with(
                signal.SIGINT,
                consumer.stop
            )
            assert signal_mock.signal.called_once_with(
                signal.SIGTERM,
                consumer.stop
            )

    def test_should_return_stopped(self):
        consumer: EventConsumer = EventConsumer()
        consumer._stopped = False
        assert consumer.stopped is False
        consumer._stopped = True
        assert consumer.stopped is True

    def test_should_initialize_kafka(self):
        with mock.patch(
            'wimpy.events.consumers.KafkaConsumer'
        ) as kafka_mock:
            kafka_consumer: mock.Mock = mock.Mock()
            kafka_mock.return_value = kafka_consumer
            consumer: EventConsumer = EventConsumer()
            assert consumer._kafka_consumer is None
            assert consumer.kafka_consumer is kafka_consumer
            assert consumer._kafka_consumer is kafka_consumer
            kafka_mock.assert_called_once_with(
                settings.ASYNC_EVENTS_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                client_id=settings.KAFKA_CONSUMER_CLIENT_ID,
                group_id=settings.KAFKA_CONSUMER_GROUP_ID,
                enable_auto_commit=settings.KAFKA_CONSUMER_AUTO_COMMIT,
                auto_offset_reset=settings.KAFKA_CONSUMER_OFFSET_RESET,
                max_poll_records=settings.KAFKA_CONSUMER_MAX_POLL_RECORDS,
                max_poll_interval_ms=settings.KAFKA_CONSUMER_MAX_POOL_INTERVAL,
                value_deserializer=deserialize_data,
            )

    def test_should_keep_kafka_connected(self):
        with mock.patch(
            'wimpy.events.consumers.KafkaConsumer'
        ) as kafka_mock:
            kafka_consumer: mock.Mock = mock.Mock()
            kafka_mock.return_value = kafka_consumer
            consumer: EventConsumer = EventConsumer()
            assert consumer.kafka_consumer is kafka_consumer
            assert consumer.kafka_consumer is kafka_consumer
            assert kafka_mock.call_count == 1

    def test_process_should_persist_event(self, valid_event_data: Dict):
        assert Event.objects.count() == 0
        consumer: EventConsumer = EventConsumer()
        consumer._process(message=valid_event_data)
        assert Event.objects.count() == 1

    def test_should_start_and_run_until_stopped(self):
        with mock.patch(
            'wimpy.events.consumers.sleep'
        ) as sleep_mock:
            sleep_mock.return_value = None
            with mock.patch.object(
                EventConsumer,
                'kafka_consumer'
            ) as kafka_consumer_mock:
                kafka_consumer_mock.poll.return_value = {}
                with mock.patch.object(
                    EventConsumer,
                    'stopped',
                    new_callable=mock.PropertyMock
                ) as stopped_mock:
                    stopped_mock.side_effect = [False, False, True]
                    consumer: EventConsumer = EventConsumer()
                    assert consumer.start() is None
                    assert kafka_consumer_mock.poll.call_count == 2
                    assert sleep_mock.call_count == 2

    def test_should_start_and_process_messages(
        self,
        valid_event_data: Dict,
        consumer_sleep_mock: mock.Mock,
        consumer_kafka_mock: mock.Mock,
        consumer_stopped_mock: mock.Mock,
        consumer_process_mock: mock.Mock,
    ):
        new_valid_event_data = copy.deepcopy(valid_event_data)
        new_valid_event_data['data']['host'] = 'some.domain'

        consumer_sleep_mock.return_value = None
        consumer_kafka_mock.poll.return_value = {
            'topic': [
                mock.Mock(value=valid_event_data),
                mock.Mock(value=new_valid_event_data)
            ]
        }
        consumer_stopped_mock.side_effect = [False, False, True]
        consumer: EventConsumer = EventConsumer()
        consumer.start()
        assert consumer_process_mock.call_count == 4
        consumer_process_mock.assert_has_calls([
            mock.call(message=valid_event_data),
            mock.call(message=new_valid_event_data),
            mock.call(message=valid_event_data),
            mock.call(message=new_valid_event_data),
        ])

    def test_should_stop(self):
        consumer: EventConsumer = EventConsumer()
        assert not consumer.stopped
        consumer.stop()
        assert consumer.stopped
