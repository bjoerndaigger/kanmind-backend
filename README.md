# Project Setup

## Installation

### Clone the repository

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
```

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create environment file

```bash
cp .env.template .env
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open the `.env` file and add your generated secret key:

```
SECRET_KEY='your-secret-key-here'
```

### Run migrations

```bash
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Start the development server

```bash
python manage.py runserver
```

## Notes

- By default, the server runs at http://127.0.0.1:8000/
- Adjust `core/settings.py` for database configuration, `DEBUG`, and `ALLOWED_HOSTS` as needed.