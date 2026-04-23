#!/bin/sh
set -e # Stops script if a command fails

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create superuser from environment variables (non-interactive)
python manage.py createsuperuser --no-input || true

## Start production server
# gunicorn core.wsgi:application --bind 0.0.0.0:${APPLICATION_PORT} --workers 3

# Start development server (enables live reload, comment out in production)
gunicorn core.wsgi:application --bind 0.0.0.0:${APPLICATION_PORT} --workers 3 --reload