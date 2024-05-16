import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from invoice.models import Freelancer, Client as Invoice_Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(client, django_user_model):
    username = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)

    client.login(username=username, password=password)

    return user

@pytest.fixture
def freelancer(user):
    freelancer = Freelancer.objects.create(name="name", address="test address", email="test@gmail.com", contact="999888777", user=user)
    return freelancer

@pytest.fixture
def invoice_client(freelancer):
    invoice_client = Invoice_Client.objects.create(name="name", address="test address", email="test@gmail.com", contact="999888777", freelancer=freelancer)
    return invoice_client

