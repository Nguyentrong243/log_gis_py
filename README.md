# Logistics GIS

A Django-based logistics management system with GIS mapping using Leaflet.

## Features

- User registration and login with email confirmation via Mailtrap
- Role-based access control (User and Admin)
- Order creation with interactive map for location selection
- Admin dashboard for order management and approval
- Real-time map displaying warehouses, vehicles, and approved orders
- REST API for orders

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup PostgreSQL Database

- Install PostgreSQL
- Create a database named `logistics_gis`
- Update `settings.py` with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'logistics_gis',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Setup Mailtrap for Email

- Sign up at [Mailtrap](https://mailtrap.io/)
- Get SMTP credentials
- Update `settings.py`:

```python
EMAIL_HOST_USER = 'your_mailtrap_username'
EMAIL_HOST_PASSWORD = 'your_mailtrap_password'
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

After creating, set the role to 'ADMIN' in the database or via Django shell:

```bash
python manage.py shell
>>> from core.models import User
>>> user = User.objects.get(username='your_username')
>>> user.role = 'ADMIN'
>>> user.save()
```

### 6. Run the Server

```bash
python manage.py runserver
```

### 7. Access the Application

Open your browser and go to `http://127.0.0.1:8000/`

## Usage

- **Home Page**: Landing page with navigation
- **Registration**: Create account (email sent via Mailtrap)
- **Login**: Authenticate to access dashboard
- **User Dashboard**: View personal orders, create new orders by clicking on map
- **Admin Dashboard**: View all orders, approve pending orders
- **Map**: Interactive Leaflet map showing logistics data

## API Endpoints

- `GET /api/orders/`: Returns approved orders in JSON format

## Technologies Used

- Django 5.2
- PostgreSQL
- Leaflet.js for mapping
- Bootstrap 5 for UI
- Mailtrap for email testing
