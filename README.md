# Baptist Student Fellowship Alumni Management System

A comprehensive web application for connecting past and present Baptist Student Fellowship members with features including real-time chat, birthday tracking, media gallery, prayer wall, and more.

## Features

- 🔐 User Management with roles (Student, Alumnus, Admin)
- 💬 Real-time chat system
- 🎂 Birthday tracking and notifications
- 🖼️ Media gallery with event categorization
- 📢 Announcements and events
- 🙏 Prayer wall and testimony board
- 💼 Job board for alumni
- 🤝 Mentorship matching system
- 📚 Resource hub
- 🕰️ Fellowship history timeline

## Tech Stack

- **Backend**: Django 4.2 with Django REST Framework
- **Database**: MongoDB (using djongo)
- **Real-time**: Django Channels with Redis
- **Frontend**: Django templates + Bootstrap 5
- **Task Queue**: Celery with Redis

## Setup Instructions

### Using Docker (Recommended)

1. Clone the repository
2. Copy environment file: `cp .env.example .env`
3. Run with Docker Compose: `docker-compose up -d`
4. Create superuser: `docker-compose exec web python manage.py createsuperuser`
5. Access at http://localhost:8000

### Local Development

1. Install MongoDB locally
2. Install Redis
3. Create virtual environment: `python -m venv venv`
4. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

## Environment Variables

Create `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=True
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=baptist_fellowship
```

## 🔐 Admin Access

### Default Admin Credentials:
- **Username**: `bsf_admin`
- **Email**: `admin@baptiststudentfellowship.org`
- **Password**: `BSF@Admin2024!`
- **Access URL**: http://localhost:8000/admin/

⚠️ **Important**: Change the default password immediately after first login!

### Admin Features:
- User management and role assignment
- Content moderation (posts, media, prayer requests)
- Event and announcement management
- System configuration and monitoring
- Analytics and reporting

## 🎨 Features & Animations

### Green-Themed Design:
- **Primary Green**: #28a745
- **Light Green**: #A8D5BA
- **Accent Colors**: Various shades of green
- **Smooth animations** throughout the interface
- **Responsive design** for all devices

### Interactive Elements:
- **Fade-in animations** for page loads
- **Hover effects** on cards and buttons
- **Pulse animations** for important elements
- **Slide transitions** for navigation
- **Loading animations** for better UX

## 🚀 Quick Start

### Automated Setup:
```bash
# Clone the repository
git clone <repository-url>
cd BSF

# Run automated setup
python setup.py

# Start the development server
# Windows:
venv\Scripts\activate
python manage.py runserver

# macOS/Linux:
source venv/bin/activate
python manage.py runserver
```

### Access the Application:
- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/

## 📱 Application Features

### 🔐 User Management
- Role-based access (Student, Alumnus, Admin)
- Profile management with photos
- Fellowship history tracking
- Birthday notifications

### 💬 Real-time Chat
- Private messaging between users
- Group chat functionality
- Message read receipts
- Typing indicators

### 🎂 Birthday System
- Automatic birthday detection
- Dashboard birthday banners
- Email notifications
- Birthday calendar view

### 🖼️ Media Gallery
- Photo and video uploads
- Event categorization
- Admin moderation
- Responsive image gallery

### 📢 Events & Announcements
- Event creation with RSVP
- Announcement broadcasting
- Event calendar integration
- Notification system

### 🙏 Prayer Wall & Testimonies
- Prayer request submission
- Community prayer support
- Testimony sharing
- Moderated content

### 💼 Job Board
- Job posting by alumni
- Application tracking
- Category filtering
- Saved jobs feature

### 🤝 Mentorship System
- Mentor profile creation
- Mentorship matching
- Session scheduling
- Feedback system

### 📚 Resource Hub
- Document sharing
- Resource categorization
- Download tracking
- Rating system

### 🕰️ Fellowship History
- Historical timeline
- Executive history
- Milestone tracking
- Photo archives

## 🛠️ Technical Architecture

### Backend:
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Django Channels** - WebSocket support
- **Celery** - Background tasks
- **MongoDB** - Database (via djongo)
- **Redis** - Caching and message broker

### Frontend:
- **Bootstrap 5** - UI framework
- **Custom CSS** - Green-themed animations
- **Font Awesome** - Icons
- **JavaScript** - Interactive features

### Deployment:
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy
- **Supervisor** - Process management
- **WhiteNoise** - Static file serving

## 📊 System Statistics

After setup, the system includes:
- **1 Admin user** with full privileges
- **5 Sample users** (students and alumni)
- **Sample content** across all modules
- **Pre-configured categories** for all features
- **Demo data** for testing

## Logo Usage

The BSF logo appears consistently across all pages in the navigation bar and key sections, maintaining brand identity throughout the application.