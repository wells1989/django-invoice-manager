import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate
from invoice.models import Client, Invoice, Freelancer, History

@pytest.mark.django_db
def test_my_invoices_page_logged_in_view(client, user, freelancer, invoice):
    response = client.get(reverse('invoice:my_invoices'))

    assert response.status_code == 200

    assert response.wsgi_request.path == reverse('invoice:my_invoices')
    assert response.context['invoices']

    invoices = response.context['invoices']

    assert len(invoices) == 1

    # result = queryset so not iterable via normal methods
    returned_invoice = invoices.first() 
    assert returned_invoice.tag == invoice.tag

@pytest.mark.django_db
def test_my_invoices_page_logged_out_user(client, user, freelancer):
    client.logout()

    response = client.get(reverse('invoice:my_invoices'), follow=True)

    assert response.redirect_chain[0][1] == 302

    assert response.status_code == 200
    assert response.wsgi_request.path == reverse('users:login')


@pytest.mark.django_db
def test_update_invoice(client, invoice, invoice_client, freelancer):
    invoice_id = invoice.pk

    data = {
    "freelancer": freelancer.id,
    "freelancer_name": freelancer.name,
    "freelancer_address": freelancer.address,
    "freelancer_email": freelancer.email,
    "freelancer_contact": freelancer.contact,
    "client": invoice_client.id,
    "client_name": invoice_client.name,
    "client_address": invoice_client.address,
    "client_email": invoice_client.email,
    "client_contact": invoice_client.contact,
    "services": invoice.services,
    "date": invoice.date,
    "month_ending": invoice.month_ending,
    "total_hours": 10,
    "total_charge": 60,
    "currency": "EUR",
    "been_paid": True,
    "status": "sent"
    }

    response = client.post(reverse('invoice:update_invoice', kwargs={'id': invoice_id}), data)

    assert response.status_code == 302

    invoice.refresh_from_db()
    assert invoice.currency == "EUR"
    assert invoice.total_hours == 10
    assert invoice.total_charge == 60

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    # Check for the specific success message
    success_message_found = False
    for message in messages:
        if str(message) == 'invoice successfully updated':
            success_message_found = True
            break
    assert success_message_found

    history = History.objects.get(invoice=invoice.id)
    assert history.status == "sent" and history.been_paid == True


@pytest.mark.django_db
def test_delete_invoice(client, invoice, invoice_client, freelancer):
    invoice_id=invoice.pk
    response = client.post(reverse('invoice:delete_invoice', kwargs={'id': invoice_id}))

    assert response.status_code == 302

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    # Check for the specific success message
    success_message_found = False
    for message in messages:
        if str(message) == 'invoice successfully deleted':
            success_message_found = True
            break

    assert success_message_found

    try:
        invoice = Invoice.objects.get(pk=invoice_id)
    except Invoice.DoesNotExist:
        invoice = None

    assert invoice is None

@pytest.mark.django_db
def test_my_invoices_search(client, freelancer, invoice):
    data = {
        "search_start_date": "2024-06-17",
        "search_paid": "on",
        "search_status": "ready", 
    }

    response = client.post(reverse('invoice:my_invoices'), data)

    assert response.status_code == 200

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    success_message_found = False
    for message in messages:
        if 'Filtering:' in str(message):
            success_message_found = True
            break

    assert success_message_found


@pytest.mark.django_db
def test_my_invoices_empty_search(client, freelancer, invoice):

    response = client.post(reverse('invoice:my_invoices'))

    assert response.status_code == 200

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    success_message_found = False
    for message in messages:
        if str(message) == 'filters cleared':
            success_message_found = True
            break

    assert success_message_found
