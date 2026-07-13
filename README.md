# Car and Parts Management System

**Django application for managing a catalog of cars, parts, and automatic cost calculation.**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Project Description

A web application for managing an auto service or car dealership that allows:
- Maintaining a parts catalog with prices and specifications
- Managing cars and their configurations
- Automatically calculating car prices based on parts and margin
- Tracking relationships between cars and parts

### Key Features:

1. **Parts Table (Parts)** — directory of parts with:
   - Part model
   - Type (engine, transmission, body, etc.)
   - Price
   - Quantity per car
   - Additional parameters

2. **Cars Table (Cars)** — car catalog:
   - Model name
   - Set of used parts
   - Margin (markup percentage)
   - **Automatic calculation of total cost** = (sum of parts cost) × (1 + margin%)

3. **Relations Table (Car Parts)** — automatically populated table showing the composition of each car


4. **Profile Management** — user profile page with password change capability
   - Administrator creates a profile and initial password for the user
   - User can change the password to their own


5. **Access Control System** — access rights separation for different user roles
   - Some actions are available only to certain user groups
   - Access control to editing and deletion functions


6. **Editing and Deleting Records** — ability to modify and delete existing parts and car records


7. **Data Validation** — automatic validation of input data:
   - Checking for non-zero values for prices, quantities, and margins
   - Checking for non-negative values (prohibition of negative numbers)

8. **Pagination** — splitting record lists into pages with a limit of 15 records per page


9. **Django Admin Panel** — available only to administrator from the site menu
---

### Database Support

The project supports working with two types of databases:
- **SQLite** — for quick start and local development
- **PostgreSQL** — for production and learning professional tools

--

## Quick Start

### Option 1: Local Launch (recommended for development)

#### Prerequisites:
- Python 3.8 or higher
- pip
- virtualenv (recommended)

#### Installation:

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/System_cars_by_Django.git
cd System_cars_by_Django

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Navigate to the project directory
cd cars

# 6. Apply database migrations
python manage.py migrate

# 7. Create a superuser for the admin panel
python manage.py createsuperuser

# 8. (Optional) Load demo data
python manage.py load_demo_data

# 9. Run the development server
python manage.py runserver
```

**Open in browser:** http://127.0.0.1:8000/

#### Demo Data

The `load_demo_data` command creates a ready set of test data for quick familiarization with the system:
All fields in the tables are filled except the "Author" column, i.e., the username who created this record. It can be empty. It is automatically filled later depending on whether the user is logged in.

```bash
python manage.py load_demo_data
```

This command will create:
- ✅ 21 parts (engines, transmissions, bodies, wheels, interiors, etc.)
- ✅ 5 cars with various configurations
- ✅ All necessary relationships between cars and parts

Useful options:
```bash
# Clear existing data and reload
python manage.py load_demo_data --clear
```

---

### Option 1.1: Launch with PostgreSQL 🐘

If you want to use PostgreSQL instead of SQLite:

#### Windows:
```bash
# 1. Install PostgreSQL (if not already installed)
# Download from https://www.postgresql.org/download/windows/

# 2. Create .env file from template
copy env_template.txt .env
# Edit .env and replace the password

# 3. Configure

```bash
# 1. Create a database (in psql or pgAdmin)
# CREATE DATABASE cars_db;
# CREATE USER cars_user WITH PASSWORD 'your_password';
# GRANT ALL PRIVILEGES ON DATABASE cars_db TO cars_user;

# 2. Create .env file
USE_POSTGRES=True
DB_NAME=cars_db
DB_USER=cars_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run the server
python manage.py runserver

---

### Option 2: Launch with Docker

#### Prerequisites:
- Docker
- Docker Compose

#### Installation and Launch:

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/System_cars_by_Django.git
cd System_cars_by_Django

# 2. Start containers
docker-compose up --build

# 3. In a separate terminal, create a superuser
docker-compose exec web python manage.py createsuperuser
```

The application will be available at: **http://localhost:8000/**

---

## 📖 Usage

### Main URL Addresses:

| URL | Description |
|-----|-------------|
| `/` | Home page (requires authorization) |
| `/register/` | Register a new user |
| `/login/` | Login to the system |
| `/logout/` | Logout from the system |
| `/profile/` | User profile page |
| `/change-password/` | Change user password |
| `/parts/` | List of all parts (with pagination) |
| `/cars/` | List of all cars (with pagination) |
| `/addparts/` | Add a new part |
| `/addcars/` | Add a new car |
| `/editparts/<id>/` | Edit a part |
| `/editcars/<id>/` | Edit a car |
| `/deleteparts/<id>/` | Delete a part |
| `/deletecars/<id>/` | Delete a car |
| `/acessor/` | Table of relationships between cars and parts |
| `/admin/` | Django admin panel |

### Workflow:

1. **Register** or log in to the system
2. **Profile Management**: 
   - Administrator creates a user profile with an initial password
   - User can change the password via `/change-password/`
   - Viewing and managing profile is available on the `/profile/` page
3. **Add parts** via `/addparts/` or admin panel
   - When adding, the system automatically validates data (prices, quantities, margins must be positive numbers)
4. **Create a car** via `/addcars/`, selecting the needed parts and specifying the margin
   - Data validation ensures correctness of entered values
5. **The system automatically calculates** the total car cost
6. **View results** in the `/cars/` and `/acessor/` tables (lists are paginated with 15 records per page)
7. **Editing and Deleting**: 
   - Edit existing records via `/editparts/<id>/` and `/editcars/<id>/`
   - Delete records via `/deleteparts/<id>/` and `/deletecars/<id>/`
   - Access to editing and deletion functions depends on user permissions

---

## Configuration

**Currently PostgreSQL is used** in the env file USE_POSTGRES=True. 
If you need to return to SQLite, just set USE_POSTGRES=False
---

## Project Structure

```
System_cars_by_Django/
├── cars/                      # Main Django project directory
│   ├── cars/                  # Project settings
│   │   ├── settings.py        # Django configuration
│   │   ├── urls.py            # Main URL routing
│   │   └── wsgi.py            # WSGI configuration
│   ├── carsdb/                # Django application
│   │   ├── models.py          # Data models (Parts, Cars, CarPart)
│   │   ├── views.py           # Views (request handling logic)
│   │   ├── forms.py           # Forms for creating objects
│   │   ├── admin.py           # Admin panel settings
│   │   ├── urls.py            # Application URL routes
│   │   ├── templates/         # HTML templates
│   │   └── static/            # CSS, JS, images
│   └── manage.py              # Django management utility
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Instructions for building Docker image
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```


## Administration

### Access to Admin Panel:

1. Create a superuser (if not already created):
   ```bash
   python manage.py createsuperuser
   ```

2. Go to: **http://127.0.0.1:8000/admin/**

3. Log in with superuser credentials

In the admin panel you can:
- Manage users and create profiles with initial passwords for them
- Configure access rights for different user groups
- Add/edit/delete parts
- Manage cars
- View relationships between cars and parts

### Useful Management Commands:

```bash
# Create a new superuser
python manage.py createsuperuser

# Load demo data for testing
python manage.py load_demo_data

# Clear and reload demo data
python manage.py load_demo_data --clear

# Create new migrations (after changing models.py)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files (for production)
python manage.py collectstatic
```

---

