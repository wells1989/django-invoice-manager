import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from invoice.models import Freelancer

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def existing_user():
    existing_user = User.objects.create_user(username="existing_username", password="existing_password")
    return existing_user

@pytest.fixture
def existing_freelancer(existing_user):
    existing_freelancer = Freelancer.objects.create(name="name", address="test address", email="test@gmail.com", contact="999888777", user=existing_user)
    return existing_freelancer
