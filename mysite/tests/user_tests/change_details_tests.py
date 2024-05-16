import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate
from invoice.models import Freelancer

@pytest.mark.django_db
def test_change_freelancer_details(client, existing_user, existing_freelancer):
    client.force_login(existing_user)

    freelancer = Freelancer.objects.get(pk=existing_freelancer.pk)

    data = {
        "name": "new_name",
        "address": "new address, city, 0000-000",
        "email": "new_email@gmail.com",
        "contact": "111222333"
    }

    response = client.post(reverse('invoice:settings'), data)

    assert response.status_code == 302
    
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    success_message_found = False
    for message in messages:
        if str(message) == 'Settings updated successfully.':
            success_message_found = True
            break
    
    assert success_message_found

    # Refresh freelancer object to get updated data from the database
    freelancer.refresh_from_db()

    assert freelancer.name == "new_name"
    assert freelancer.address == "new address, city, 0000-000"
    assert freelancer.email == "new_email@gmail.com"
    assert freelancer.contact == "111222333"


@pytest.mark.django_db
def test_change_username(client, existing_user):
    client.force_login(existing_user)

    data = {
        "new_username": "new_username"
    }

    response = client.post(reverse('users:change_username'), data)

    assert response.status_code == 302
    assert response.url == reverse('invoice:settings')

    # refresh user object to show updates
    existing_user.refresh_from_db()
    assert existing_user.username == "new_username"

    # checking for messages in response e.g. messages.success(request, "success message")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    # Check for the specific success message
    success_message_found = False
    for message in messages:
        if str(message) == 'Username changed successfully.':
            success_message_found = True
            break

    assert success_message_found


@pytest.mark.django_db
def test_change_password(client, existing_user):
    client.force_login(existing_user)

    data = {
        "current_password": "existing_password",
        "new_password": "new_password"
    }

    response = client.post(reverse('users:change_password'), data)

    assert response.status_code == 302
    
    assert response.url == reverse('invoice:settings')

    # refresh user object to show updates
    existing_user.refresh_from_db()
    
    # testing login
    user = authenticate(username=existing_user.username, password="new_password")
    assert user is not None

    # checking for messages in response e.g. messages.success(request, "success message")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0

    # Check for the specific success message
    success_message_found = False
    for message in messages:
        if str(message) == 'Password changed successfully.':
            success_message_found = True
            break
    
    assert success_message_found