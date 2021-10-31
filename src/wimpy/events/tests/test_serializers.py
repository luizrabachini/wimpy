import pytest

from wimpy.events.serializers import EventSerializer


@pytest.mark.django_db
class TestEventSerializer:

    def test_should_create_event_id(self, valid_event_data):
        serializer: EventSerializer = EventSerializer(data=valid_event_data)
        assert serializer.is_valid()
        assert serializer.data['event_id']

    @pytest.mark.parametrize(
        'field,value',
        [
            ('application_id', ''),
            ('session_id', ''),
            ('category', ''),
            ('name', ''),
            ('data', ''),
            ('timestamp', '01/06/2017 18:43:26'),
        ]
    )
    def test_should_validate_fields(self, field, value, valid_event_data):
        valid_event_data[field] = value
        serializer: EventSerializer = EventSerializer(data=valid_event_data)
        assert not serializer.is_valid()
