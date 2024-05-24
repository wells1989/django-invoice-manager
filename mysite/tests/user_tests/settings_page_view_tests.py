import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_settings_page_with_logged_in_user(client, existing_user, existing_freelancer):

    client.force_login(existing_user)

    response = client.get(reverse('invoice:settings'))

    assert response.status_code == 200
    assert response.wsgi_request.path == reverse('invoice:settings')

@pytest.mark.django_db
def test_settings_page_without_logged_in_user(client, existing_user):
    client.logout()

    response = client.get(reverse('invoice:settings'), follow=True) # follow needed to get access to final url not first one in the redirect chain

    # checking first redirect
    assert response.redirect_chain[0][1] == 302

    # checking final redirect destination
    assert response.status_code == 200
    assert response.wsgi_request.path == reverse('users:login')
