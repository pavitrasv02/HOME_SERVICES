# 🏠 Home Services Web Application

A full-stack Django-based Home Services web application that allows users to browse and book household services such as cleaning, cooking, gardening, maintenance, and home automation.

The platform provides a simple booking workflow, service listings, menu management, provider reviews, and an admin dashboard for managing the application.

---

# 📌 Features

## ✅ Service Categories

The platform supports multiple home service categories:

- 🧹 Cleaning Services
- 🍳 Cooking Services
- 🌱 Gardening Services
- 🔧 Maintenance Services
- 🤖 Home Automation Services

---

## ✅ Booking System

Users can:

- Browse available services
- Select preferred service
- Choose booking time/date
- Enter service address
- Place bookings

---

## ✅ Menu & Dish Management

Supports:

- Food menu listings
- Dish management
- Sample menu population scripts
- Pricing display

---

## ✅ Reviews & Ratings

Customers and providers can:

- Leave reviews
- Give ratings
- Read feedback

---

## ✅ Django Admin Panel

Admin can manage:

- Services
- Bookings
- Reviews
- Users
- Menu items

---

# 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | Backend Language |
| Django | Web Framework |
| SQLite | Development Database |
| HTML/CSS | Frontend UI |
| JavaScript | Dynamic Features |
| Django Templates | Server-side Rendering |
| WhiteNoise | Static File Serving |
| PostgreSQL | Recommended Production DB |

---

# 📂 Project Structure

```bash
home_services/
│
├── manage.py
├── settings.py
├── urls.py
├── wsgi.py
├── asgi.py
├── requirements.txt
├── ProcFile
├── db.sqlite3
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   │
│   ├── templates/
│   │   └── core/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── services.html
│   │       └── booking.html
│   │
│   ├── management/
│   │   └── commands/
│   │       ├── add_menu_items.py
│   │       ├── add_cleaning_services.py
│   │       ├── add_cooking_services.py
│   │       ├── add_gardening_services.py
│   │       ├── add_maintenance_services.py
│   │       └── add_automation_services.py
│   │
│   └── migrations/
│
├── static/
├── staticfiles/
│
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd home_services
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/Mac

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Migrations

```bash
python manage.py migrate
```

---

## 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

## 6️⃣ Seed Sample Data

```bash
python manage.py add_menu_items
python manage.py add_cleaning_services
python manage.py add_cooking_services
python manage.py add_gardening_services
python manage.py add_maintenance_services
python manage.py add_automation_services
```

---

## 7️⃣ Start Development Server

```bash
python manage.py runserver
```

Open browser:

```bash
http://127.0.0.1:8000/
```

---

# 🧠 Project Architecture

This project follows Django’s **MVT (Model-View-Template)** architecture.

## 🔹 Model

Handles database structure and ORM.

Example:

```python
class Service(models.Model):
    name = models.CharField(max_length=100)
```

---

## 🔹 View

Contains business logic.

Responsibilities:

- Handle requests
- Process forms
- Save bookings
- Render pages

---

## 🔹 Template

Frontend HTML pages rendered dynamically using Django templates.

---

# 🔄 Application Workflow

```text
User Request
     ↓
URL Routing
     ↓
View Logic
     ↓
Database Models
     ↓
Template Rendering
     ↓
Response to User
```

---

# 🗄️ Database Overview

## Main Tables

### Users

Stores:

- Username
- Email
- Password

---

### Services

Stores:

- Service Name
- Category
- Price
- Description

---

### Bookings

Stores:

- User Details
- Booking Date/Time
- Address
- Service Selected
- Status

---

### Reviews

Stores:

- Ratings
- Comments
- Review Timestamp

---

# 🧪 Running Tests

Run tests using:

```bash
python manage.py test
```

You can add:

- Unit Tests
- Integration Tests
- Form Validation Tests
- Booking Flow Tests

---

# 🌐 Deployment Guide

## Recommended Production Stack

| Component | Recommendation |
|-----------|---------------|
| App Server | Gunicorn |
| Database | PostgreSQL |
| Hosting | Render / Railway / Heroku |
| Static Files | WhiteNoise |
| Reverse Proxy | Nginx |

---

# 🚀 Production Configuration

## Disable Debug Mode

```python
DEBUG = False
```

---

## Configure Allowed Hosts

```python
ALLOWED_HOSTS = ['yourdomain.com']
```

---

## Collect Static Files

```bash
python manage.py collectstatic
```

---

## Use Environment Variables

Recommended package:

```bash
pip install python-dotenv
```

Example `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-db-url
```

---

# 🔐 Security Recommendations

For production deployment:

- Use HTTPS
- Secure secret keys
- Add authentication protection
- Validate user input
- Configure secure cookies
- Prevent spam bookings
- Use PostgreSQL instead of SQLite

---

# 📈 Future Improvements

## Planned Features

- 🔑 User Authentication System
- 💳 Online Payment Integration
- 📍 Google Maps Integration
- 📱 Responsive Mobile UI
- 🔔 Email Notifications
- 🤖 AI-based Service Recommendations
- 📊 Provider Dashboard
- 💬 Live Chat Support
- 📦 Docker Support
- ⚡ REST API using Django REST Framework

---

# 💡 Why This Project?

This project demonstrates:

- Full-stack web development
- Django architecture understanding
- CRUD operations
- Database management
- Backend development
- Dynamic templates
- Deployment knowledge
- Real-world business workflow

Perfect for:

- College projects
- Portfolio projects
- Internship applications
- Placement interviews

---

# 📜 Management Commands

Run commands using:

```bash
python manage.py <command_name>
```

## Available Commands

| Command | Purpose |
|---------|---------|
| add_menu_items | Add sample menu items |
| add_cleaning_services | Add cleaning services |
| add_cooking_services | Add cooking services |
| add_gardening_services | Add gardening services |
| add_maintenance_services | Add maintenance services |
| add_automation_services | Add automation services |

---

# 🧹 Troubleshooting

## Static Files Not Loading

Run:

```bash
python manage.py collectstatic
```

---

## Migration Errors

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Seeder Errors

Ensure:

- Models match seeder fields
- Migrations are applied properly

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Developed by **Pavitra S V**

Computer Science Student | Full Stack Developer | Django Enthusiast

---

# ⭐ Acknowledgements

Special thanks to:

- Django Documentation
- Open Source Community
- Python Community

---

# 📬 Contact

For suggestions or collaboration:

- GitHub: your-github-link
- LinkedIn: your-linkedin-link

---

# 🎯 Final Note

This project is designed as a real-world home services booking platform and serves as an excellent demonstration of Django full-stack development concepts including:

- Backend architecture
- Database integration
- Dynamic rendering
- CRUD functionality
- Deployment workflow
- Management commands
- Production setup basics
