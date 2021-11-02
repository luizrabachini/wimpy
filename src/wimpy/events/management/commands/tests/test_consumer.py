from unittest import mock

from wimpy.events.management.commands.consumer import Command


class TestCommand:

    def test_should_start_consumer(self, caplog):
        with mock.patch(
            'wimpy.events.management.commands.consumer.EventConsumer'
        ) as mock_event_consumer:
            consumer: mock.Mock = mock.Mock()
            mock_event_consumer.return_value = consumer
            command: Command = Command()
            assert command.handle() is None
            assert mock_event_consumer.called
            assert consumer.start.called
            assert 'Starting events consumer' in caplog.text
            assert 'Events consumer finished' in caplog.text
