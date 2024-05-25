#!/bin/sh

# Run database migrations
python manage.py migrate

# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 mysite.wsgi