import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_view(client, freelancer, user):

    response = client.get(reverse('invoice:home'))

    assert response.status_code == 200
    assert response.wsgi_request.path == reverse('invoice:home')


@pytest.mark.django_db
def test_other_page_views(client, freelancer, user):

    routes = [reverse('invoice:settings'), reverse('invoice:my_invoices'), reverse('invoice:new_invoice'), reverse('invoice:history'), reverse('invoice:statistics')]

    for route in routes:
        response = client.get(route)

        assert response.status_code == 200
        assert response.wsgi_request.path == route
