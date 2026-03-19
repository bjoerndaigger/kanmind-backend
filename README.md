# Project Setup

Two setup methods are available — choose one.

---

## Option A: Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/bjoerndaigger/kanmind-backend
cd kanmind-backend
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.template .env
```

Generate a secret key and copy the output:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add it to your `.env` file:
```
SECRET_KEY='your-secret-key-here'
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

---

## Option B: Docker Setup

### 1. Clone the repository
```bash
git clone https://github.com/bjoerndaigger/kanmind-backend
cd kanmind-backend
```

### 2. Configure environment

Copy `.env.template` to `.env` and replace the placeholder values with your own.
```bash
cp .env.template .env
```

### 3. Start all services
```bash
docker compose up --build
```

This will automatically build the image, apply migrations, and start the server.

### 4. Stop all services
```bash
docker compose down
```

---

## Notes

- The server runs at **http://127.0.0.1:8000/** by default.
- Adjust `core/settings.py` for `DEBUG`, `ALLOWED_HOSTS`, and database configuration.