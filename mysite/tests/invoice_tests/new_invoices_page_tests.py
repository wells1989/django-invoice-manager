import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from invoice.models import Client, Invoice

# creating a client
@pytest.mark.django_db
def test_create_client(client, freelancer, user):
    data = {
        "freelancer": freelancer,
        "name": "client_unique_name",
        "address": "client address",
        "email": "client@gmail.com",
        "contact": "999777666"
    }

    response = client.post(reverse('invoice:create_client'), data)

    assert response.status_code == 200

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    # Check for the specific success message
    success_message_found = False
    for message in messages:
        if str(message) == 'Client successfully added.':
            success_message_found = True
            break

    assert success_message_found

    assert Client.objects.get(name="client_unique_name")

# deleting a client
@pytest.mark.django_db
def test_delete_client(client, freelancer, user):
    original_client = Client.objects.create(freelancer=freelancer, name="client_name", address="sample address", email="sample@gmail.com", contact="111222333")
    
    deleted_client_id = original_client.pk

    response = client.delete(reverse('invoice:delete_client', kwargs={'id': deleted_client_id})) # i.e. invoice/delete_client/<int:id>

    assert response.status_code == 302

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    # Check for the specific success message
    success_message_found = False
    for message in messages:
        if str(message) == 'client successfully deleted':
            success_message_found = True
            break

    assert success_message_found

    try:
        client = Client.objects.get(pk=deleted_client_id)
    except Client.DoesNotExist:
        client = None

    assert client is None

# creating an invoice
@pytest.mark.django_db
def test_creating_invoice(client, freelancer, user, invoice_client):
    data = {
        "client": invoice_client.id,
        "client_name": invoice_client.name,
        "client_address": invoice_client.address,
        "client_email": invoice_client.email,
        "client_contact": invoice_client.contact,
        
        "freelancer": freelancer.id,
        "freelancer_name": freelancer.name,
        "freelancer_address": freelancer.address,
        "freelancer_email": freelancer.email,
        "freelancer_contact": freelancer.contact,
        
        "date": "2024-05-20T12:00:00Z",
        "month_ending": "2024-06-20T12:00:00Z",
        "services": "Sample services description",
        "total_hours": 40.00,
        "total_charge": 4000.00,
        "currency": "EUR",
        "been_paid": "",
        "status": "ready"
    }

    response = client.post(reverse('invoice:new_invoice'), data)

    assert response.status_code == 200

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    message_found = False
    for message in messages:
        if str(message) == "Invoice successfully added.":
            message_found = True
            break
    assert message_found

    assert Invoice.objects.get(date="2024-05-20T12:00:00Z",services="Sample services description")
    
