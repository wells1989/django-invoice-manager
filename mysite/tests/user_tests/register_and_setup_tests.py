import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

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
def test_duplicate_register(client, existing_client):
    response = client.post(reverse('users:register'), {
        'username': existing_client.username,
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
def test_setup_view(client):
    user = User.objects.create_user(username='test_user', password='test_password')
    client.force_login(user)
    response = client.get(reverse('users:setup'))
    assert response.status_code == 200
