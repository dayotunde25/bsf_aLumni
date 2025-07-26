# Baptist Student Fellowship Alumni Management System
## Complete Installation Guide

### 🎯 System Overview
A comprehensive web application for connecting past and present Baptist Student Fellowship members with features including real-time chat, birthday tracking, media gallery, prayer wall, job board, mentorship system, and more.

### 🛠️ Tech Stack
- **Backend**: Django 4.2 with Django REST Framework
- **Database**: MongoDB (using djongo)
- **Real-time**: Django Channels with Redis
- **Frontend**: Django templates + Bootstrap 5 + Custom CSS with animations
- **Task Queue**: Celery with Redis

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB Community Server
- Redis Server
- Git

### Step 1: Install Prerequisites

#### Windows:
1. **Python**: Download from [python.org](https://python.org)
2. **MongoDB**: Download from [mongodb.com](https://www.mongodb.com/try/download/community)
3. **Redis**: Download from [redis.io](https://redis.io/download) or use WSL
4. **Git**: Download from [git-scm.com](https://git-scm.com)

#### macOS:
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install prerequisites
brew install python mongodb-community redis git
```

#### Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install mongodb-org

# Install Redis
sudo apt install redis-server
```

### Step 2: Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd BSF

# Run the automated setup script
python setup.py
```

### Step 3: Manual Setup (Alternative)

If the automated setup fails, follow these manual steps:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py create_admin

# Create sample data
python manage.py create_sample_data

# Collect static files
python manage.py collectstatic --noinput
```

### Step 4: Start Services

#### Start MongoDB:
```bash
# Windows (if installed as service):
net start MongoDB

# macOS:
brew services start mongodb-community

# Ubuntu/Linux:
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### Start Redis:
```bash
# Windows (if installed):
redis-server

# macOS:
brew services start redis

# Ubuntu/Linux:
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Start Django Development Server:
```bash
# Activate virtual environment first
python manage.py runserver
```

### Step 5: Access the Application

- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/

#### Admin Login Details:
- **Username**: `bsf_admin`
- **Email**: `admin@baptiststudentfellowship.org`
- **Password**: `BSF@Admin2024!`
- ⚠️ **Please change the password after first login!**

---

## 🌐 Production Deployment

### Option 1: Heroku Deployment

#### Prerequisites:
- Heroku CLI installed
- Git repository

#### Steps:
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add MongoDB Atlas addon
heroku addons:create mongolab:sandbox

# Add Redis addon
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set MONGO_URI="your-mongodb-atlas-uri"
heroku config:set MONGO_DB_NAME="baptist_fellowship"

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create admin user
heroku run python manage.py create_admin

# Create sample data (optional)
heroku run python manage.py create_sample_data
```

### Option 2: DigitalOcean Droplet

#### Prerequisites:
- DigitalOcean account
- Domain name (optional)

#### Steps:

1. **Create Droplet**:
   - Choose Ubuntu 20.04 LTS
   - Select appropriate size (minimum 2GB RAM)
   - Add SSH key

2. **Connect and Setup**:
```bash
# Connect to droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install prerequisites
apt install python3 python3-pip python3-venv nginx git supervisor -y

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
apt update
apt install mongodb-org -y

# Install Redis
apt install redis-server -y

# Start services
systemctl start mongod
systemctl enable mongod
systemctl start redis-server
systemctl enable redis-server
```

3. **Deploy Application**:
```bash
# Clone repository
cd /var/www
git clone <repository-url> bsf
cd bsf

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Setup environment
cp .env.example .env
# Edit .env with production settings

# Run migrations and setup
python manage.py migrate
python manage.py create_admin
python manage.py collectstatic --noinput

# Create gunicorn service
nano /etc/systemd/system/bsf.service
```

4. **Gunicorn Service Configuration** (`/etc/systemd/system/bsf.service`):
```ini
[Unit]
Description=Baptist Student Fellowship Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bsf
Environment="PATH=/var/www/bsf/venv/bin"
ExecStart=/var/www/bsf/venv/bin/gunicorn --workers 3 --bind unix:/var/www/bsf/bsf.sock baptist_fellowship.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Nginx Configuration** (`/etc/nginx/sites-available/bsf`):
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/bsf;
    }
    
    location /media/ {
        root /var/www/bsf;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/bsf/bsf.sock;
    }
}
```

6. **Enable and Start Services**:
```bash
# Enable Nginx site
ln -s /etc/nginx/sites-available/bsf /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx

# Start application
systemctl start bsf
systemctl enable bsf

# Check status
systemctl status bsf
```

### Option 3: AWS EC2 Deployment

Similar to DigitalOcean but with AWS-specific configurations:

1. **Launch EC2 Instance**:
   - Choose Ubuntu 20.04 LTS AMI
   - Select t3.medium or larger
   - Configure security groups (HTTP, HTTPS, SSH)

2. **Setup MongoDB Atlas**:
   - Create MongoDB Atlas cluster
   - Get connection string
   - Update environment variables

3. **Setup Redis ElastiCache**:
   - Create Redis cluster
   - Update Redis URL in settings

4. **Follow similar deployment steps as DigitalOcean**

---

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=baptist_fellowship
REDIS_URL=redis://localhost:6379
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### MongoDB Configuration
- Default database: `baptist_fellowship`
- Collections are created automatically by Django

### Redis Configuration
- Used for Django Channels (WebSocket support)
- Used for Celery task queue
- Default: `redis://localhost:6379`

---

## 🧪 Testing

### Run Tests
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test events
```

### Load Testing
```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_test.py --host=http://localhost:8000
```

---

## 🔍 Troubleshooting

### Common Issues:

1. **MongoDB Connection Error**:
   - Ensure MongoDB is running
   - Check connection string in .env
   - Verify firewall settings

2. **Redis Connection Error**:
   - Ensure Redis is running
   - Check Redis URL in settings
   - Verify Redis configuration

3. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings
   - Verify Nginx configuration in production

4. **Permission Errors**:
   - Check file permissions
   - Ensure www-data user has access
   - Verify virtual environment activation

### Logs:
```bash
# Django logs
tail -f /var/log/nginx/error.log
journalctl -u bsf -f

# MongoDB logs
tail -f /var/log/mongodb/mongod.log

# Redis logs
tail -f /var/log/redis/redis-server.log
```

---

## 📞 Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation wiki

---

## 🔐 Security Notes

1. **Change default passwords** immediately after installation
2. **Use HTTPS** in production
3. **Keep dependencies updated**
4. **Regular backups** of MongoDB data
5. **Monitor logs** for suspicious activity
6. **Use environment variables** for sensitive data
