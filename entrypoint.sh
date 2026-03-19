# Apply database migrations
python manage.py migrate

# Create superuser from environment variables (non-interactive)
python manage.py createsuperuser --no-input

# Start development server on all interfaces
python manage.py runserver 0.0.0.0:${APPLICATION_PORT}