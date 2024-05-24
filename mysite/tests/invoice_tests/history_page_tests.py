import pytest
from invoice.views import history
from django.urls import reverse

@pytest.mark.django_db
def test_history_view_get(user, freelancer, client, history, invoice):

    response = client.get(reverse('invoice:history'))
    
    assert response.status_code == 200
    
    # checking context is not empty
    assert response.context['history']
    assert response.context['invoices']

@pytest.mark.django_db
def test_history_page_without_logged_in_user(client, user):
    client.logout()

    response = client.get(reverse('invoice:history'), follow=True)

    assert response.redirect_chain[0][1] == 302

    assert response.status_code == 200
    assert response.wsgi_request.path == reverse('users:login')

@pytest.mark.django_db
def test_history_view_post(user, client, freelancer, invoice, history):

    data = {'tag': invoice.tag, 'invoice_id': invoice.id}

    response = client.post(reverse('invoice:history'), data)
    
    assert response.status_code == 200
    
    assert response.context['invoices']
    assert response.context['history']

    
