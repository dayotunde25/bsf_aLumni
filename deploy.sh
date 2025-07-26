#!/bin/bash

# Baptist Student Fellowship Alumni Management System Deployment Script
# This script automates the deployment process for production servers

set -e  # Exit on any error

echo "🚀 Baptist Student Fellowship Deployment Script"
echo "================================================"

# Configuration
PROJECT_DIR="/var/www/bsf"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="bsf"
NGINX_SITE="bsf"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Function to check if service exists
service_exists() {
    systemctl list-units --full -all | grep -Fq "$1.service"
}

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages if not present
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx git supervisor mongodb-org redis-server

# Create project directory if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    print_status "Creating project directory..."
    sudo mkdir -p "$PROJECT_DIR"
    sudo chown $USER:$USER "$PROJECT_DIR"
fi

# Navigate to project directory
cd "$PROJECT_DIR"

# Pull latest code
if [ -d ".git" ]; then
    print_status "Pulling latest code..."
    git pull origin main
else
    print_error "Git repository not found. Please clone the repository first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install/update Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your production settings"
    read -p "Press enter to continue after editing .env file..."
fi

# Run Django management commands
print_status "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Create admin user if it doesn't exist
print_status "Creating admin user..."
python manage.py create_admin

# Create sample data (optional)
read -p "Do you want to create sample data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Creating sample data..."
    python manage.py create_sample_data
fi

# Set proper permissions
print_status "Setting file permissions..."
sudo chown -R www-data:www-data "$PROJECT_DIR"
sudo chmod -R 755 "$PROJECT_DIR"

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Baptist Student Fellowship Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --workers 3 --bind unix:$PROJECT_DIR/$SERVICE_NAME.sock baptist_fellowship.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
print_status "Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/$NGINX_SITE > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $PROJECT_DIR;
    }
    
    location /media/ {
        root $PROJECT_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/$SERVICE_NAME.sock;
    }
}
EOF

# Enable Nginx site
if [ ! -L "/etc/nginx/sites-enabled/$NGINX_SITE" ]; then
    print_status "Enabling Nginx site..."
    sudo ln -s /etc/nginx/sites-available/$NGINX_SITE /etc/nginx/sites-enabled/
fi

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Start and enable services
print_status "Starting services..."

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Reload systemd and start application
sudo systemctl daemon-reload
sudo systemctl start $SERVICE_NAME
sudo systemctl enable $SERVICE_NAME

# Restart Nginx
sudo systemctl restart nginx

# Check service status
print_status "Checking service status..."
if systemctl is-active --quiet $SERVICE_NAME; then
    print_status "Application service is running"
else
    print_error "Application service failed to start"
    sudo systemctl status $SERVICE_NAME
    exit 1
fi

if systemctl is-active --quiet nginx; then
    print_status "Nginx is running"
else
    print_error "Nginx failed to start"
    sudo systemctl status nginx
    exit 1
fi

# Display final information
echo
echo "🎉 Deployment completed successfully!"
echo "=================================="
echo
echo "📋 Admin User Details:"
echo "   Username: bsf_admin"
echo "   Email: admin@baptiststudentfellowship.org"
echo "   Password: BSF@Admin2024!"
echo "   ⚠️  Please change the password after first login!"
echo
echo "🌐 Application URLs:"
echo "   Main Site: http://$(hostname -I | awk '{print $1}')"
echo "   Admin Panel: http://$(hostname -I | awk '{print $1}')/admin/"
echo
echo "🔧 Useful Commands:"
echo "   Check app status: sudo systemctl status $SERVICE_NAME"
echo "   Restart app: sudo systemctl restart $SERVICE_NAME"
echo "   View app logs: sudo journalctl -u $SERVICE_NAME -f"
echo "   Check Nginx status: sudo systemctl status nginx"
echo "   View Nginx logs: sudo tail -f /var/log/nginx/error.log"
echo
echo "📁 Project Location: $PROJECT_DIR"
echo "🔐 Remember to configure SSL/HTTPS for production!"
