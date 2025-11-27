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