import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from invoice.views import history
from django.urls import reverse

@pytest.mark.django_db
def test_history_view_get(user, freelancer, client):

    response = client.get(reverse('invoice:history'))
    
    assert response.status_code == 200
    
    assert 'history' in response.context
    assert 'invoices' in response.context


@pytest.mark.django_db
def test_history_view_post(user, client, freelancer, invoice):

    data = {'tag': 'example_tag', 'invoice_id': 1}

    response = client.post(reverse('invoice:history'), data)
    
    assert response.status_code == 200
    
    assert 'history' in response.context
    assert 'invoices' in response.context
    
