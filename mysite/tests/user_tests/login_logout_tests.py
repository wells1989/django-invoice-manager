import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from urllib.parse import urlparse, parse_qs

@pytest.mark.django_db
def test_custom_login_view(client):
    user = User.objects.create_user(username='test_user', password='test_password')
    
    login_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    login_response = client.post(reverse('users:login'), login_data)

    # Verify that login is successful
    assert login_response.status_code == 302

    # Check if the user is logged in
    user = login_response.wsgi_request.user # sends back the request.user associated with the login_response
    assert user.is_authenticated # checks they're authenticated


@pytest.mark.django_db
def test_incorrect_login(client):
    response = client.post(reverse('users:login'), {
        'username': 'incorrect_user',
        'password': 'incorrect_password'
    })
    assert response.status_code == 200

    # when unsure about the key of the form error message, only the end value
    form = response.context['form']
    
    error_message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
    error_message_found = False
    for field_errors in form.errors.values():
        if error_message in field_errors:
            error_message_found = True
            break

    assert error_message_found


@pytest.mark.django_db
def test_logout_view(client):
    user = User.objects.create_user(username='test_user', password='test_password')
    client.login(username='test_user', password='test_password')

    response = client.post(reverse('users:logout'))

    assert response.status_code == 200

    # making a request to a @login_required route
    response = client.get(reverse('invoice:home'))

    # Verify that the user is redirected to the login page
    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login')) 

    parsed_url = urlparse(response.url)

    query_params = parse_qs(parsed_url.query)

    assert 'next' in query_params


