import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_page_without_logged_in_user(client, user):
    client.logout()

    response = client.get(reverse('invoice:home'), follow=True)

    assert response.redirect_chain[0][1] == 302

    assert response.status_code == 200
    assert response.wsgi_request.path == reverse('users:login')

@pytest.mark.django_db
def test_homepage_view(client, freelancer, invoice):
    response = client.get(reverse('invoice:home'))

    assert response.status_code == 200

    fields = ['invoice_count', 'currencies', 'months'] 
    assert all(field in response.context for field in fields)
    assert response.context['invoice_count'] == 1

    assert response.context['currencies']['USD'] == 30
    assert len(response.context['months'].keys()) > 0


