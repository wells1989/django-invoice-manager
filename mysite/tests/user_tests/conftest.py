import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def existing_client():
    existing_client = User.objects.create_user(username="existing_username", password="existing_password")
    return existing_client
