import pytest
from django.test import override_settings
from django.urls import reverse

ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'


@pytest.mark.django_db
class TestAuth:

    @override_settings(CORS_ALLOWED_ORIGINS=['http://domain.com'])
    def test_should_accept_request_from_allowed_origin(self, client):
        response = client.options(
            reverse('events:events'),
            HTTP_ORIGIN='http://domain.com'
        )
        assert response[ACCESS_CONTROL_ALLOW_ORIGIN] == 'http://domain.com'

    @override_settings(CORS_ALLOWED_ORIGINS=['http://domain.com'])
    def test_should_not_accept_request_from_not_allowed_origin(self, client):
        response = client.options(
            reverse('events:events'),
            HTTP_ORIGIN='http://test.com'
        )
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in response

    @override_settings(CORS_ALLOW_ALL_ORIGINS=True)
    def test_should_accept_request_from_all_origins(self, client):
        response = client.options(
            reverse('events:events'),
            HTTP_ORIGIN='http://test.com'
        )
        assert response[ACCESS_CONTROL_ALLOW_ORIGIN] == '*'
