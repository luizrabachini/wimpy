import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestEventAPIView:

    def test_should_create_event(self, valid_event_data, auth_client):
        response = auth_client.post(
            reverse('events:events'),
            valid_event_data,
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        'field,value',
        [
            ('session_id', ''),
            ('category', ''),
            ('name', ''),
            ('data', ''),
            ('timestamp', '01/06/2017 18:43:26'),
        ]
    )
    def test_should_return_bad_request(
        self,
        field,
        value,
        valid_event_data,
        auth_client
    ):
        valid_event_data[field] = value
        response = auth_client.post(
            reverse('events:events'),
            valid_event_data,
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
