from typing import Dict

import pytest
from django.contrib.auth.models import User
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username='john.doe',
        email='john.doe@localhost',
        password='potato123'
    )


@pytest.fixture
def token(user) -> Dict:
    token = RefreshToken.for_user(user=user)
    return token


@pytest.fixture
def access_token(token) -> str:
    return str(token.access_token)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def auth_client(client, access_token):
    return Client(HTTP_AUTHORIZATION=f'Bearer {access_token}')
