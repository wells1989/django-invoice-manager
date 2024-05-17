import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from invoice.models import Freelancer, Client as Invoice_Client, Invoice
from django.utils import timezone

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


@pytest.fixture
def invoice(freelancer, invoice_client):
    invoice = Invoice.objects.create(freelancer=freelancer, freelancer_name=freelancer.name, freelancer_address=freelancer.address, freelancer_email=freelancer.email, freelancer_contact=freelancer.contact,
                                     client=invoice_client, client_name=invoice_client.name, client_address=invoice_client.address, client_email=invoice_client.email, client_contact=invoice_client.contact,
                                     services='1. test service, 5, 6', date="2024-06-17", month_ending="2024-05-17", total_hours=5, total_charge=30, currency='USD', been_paid=False, status='ready')
    return invoice



