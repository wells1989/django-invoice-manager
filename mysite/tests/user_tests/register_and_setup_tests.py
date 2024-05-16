import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from invoice.models import Freelancer

@pytest.mark.django_db
def test_register_view(client):
    response = client.post(reverse('users:register'), {
        'username': 'test_user',
        'password1': 'test_password',
        'password2': 'test_password'
    })
    assert response.status_code == 302
    assert User.objects.filter(username='test_user').exists()

@pytest.mark.django_db
def test_duplicate_register(client, existing_user):
    response = client.post(reverse('users:register'), {
        'username': existing_user.username,
        'password1': 'existing_password',
        'password2': 'existing_password'
    })

    assert 'form' in response.context
    
    form = response.context['form']
    assert form.errors
    assert 'username' in form.errors 
    assert 'A user with that username already exists.' in form.errors['username']

@pytest.mark.django_db
def test_register_incorrect_field_values(client):
    response = client.post(reverse('users:register'), {
        'username': 'test',
        'password1': 'pass',
        'password2': 'pass'
    })

    assert response.status_code == 200
    form = response.context['form']

    error_message_1 = "This password is too short. It must contain at least 8 characters."
    error_message_2 = "This password is too common."

    error_message_matches = 0
    for field_errors in form.errors.values():
        if error_message_1 in field_errors or error_message_2 in field_errors:
            error_message_matches +=1

    assert error_message_matches in [1,2]

@pytest.mark.django_db
def test_setup_view(client, existing_user):
    client.force_login(existing_user)
    response = client.get(reverse('users:setup'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_valid_setup(client, existing_user):
    client.force_login(existing_user)

    data = {
        "name": "test_name",
        "address": "sample address, city, 0000-000",
        "email": "sample@gmail.com",
        "contact": "999 777 888"
    }

    response = client.post(reverse('users:setup'), data)

    assert response.status_code == 302
    assert (response.url == reverse("invoice:home"))
    
    assert Freelancer.objects.filter(name='test_name').exists()


@pytest.mark.django_db
def test_invalid_setup(client, existing_user):
    client.force_login(existing_user)

    data = {
        "name": "test_name",
        "address": "sample address, city, 0000-000",
        "email": "sample@gmail.com"
    }

    response = client.post(reverse('users:setup'), data)

    assert response.status_code == 200

    # checking for current url (response.url == reverse('users:setup')) only works on redirects
    assert response.wsgi_request.path == reverse('users:setup')

    form = response.context['form']
    assert form is not None

    error_count = 0
    for error in form.errors.values():
        error_count += 1
    
    assert error_count >= 1
    
    assert not Freelancer.objects.filter(name='test_name').exists()

