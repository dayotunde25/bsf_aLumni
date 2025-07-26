# Deploying to Render

This guide will walk you through the process of deploying the Baptist Student Fellowship Alumni Management System to Render.

## 1. Prerequisites

*   A Render account.
*   A GitHub account with the project repository.

## 2. Prepare the Application for Production

Before deploying, you need to make a few changes to the application to get it ready for a production environment.

### 2.1. Create a `render.yaml` file

Create a file named `render.yaml` in the root of your project. This file will tell Render how to build and run your application.

```yaml
services:
  - type: web
    name: bsf-alumni
    env: python
    plan: free
    buildCommand: |
      pip install -r requirements.txt
      python manage.py migrate
    startCommand: gunicorn baptist_fellowship.wsgi
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: WEB_CONCURRENCY
        value: 4
```

### 2.2. Update `baptist_fellowship/settings.py`

You need to make some changes to your `settings.py` file to work with Render's environment.

*   **`ALLOWED_HOSTS`**: Add your Render app's URL to the `ALLOWED_HOSTS` list. You can use a wildcard to allow all `onrender.com` subdomains.
*   **`DATABASES`**: Configure the database to use the `DATABASE_URL` environment variable provided by Render.
*   **`STATIC_ROOT`**: Ensure `STATIC_ROOT` is set correctly for collecting static files.

Here's an example of the changes you need to make:

```python
# baptist_fellowship/settings.py

import os
from pathlib import Path
from decouple import config
import dj_database_url

# ...

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com', '.onrender.com']

# ...

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3')
    )
}

# ...

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# ...
```

### 2.3. Add `gunicorn` to `requirements.txt`

Render uses the `gunicorn` web server to run Python applications. Add it to your `requirements.txt` file:

```
gunicorn
```

## 3. Deploy to Render

1.  **Push your changes to GitHub**: Make sure your `render.yaml` file and updated `settings.py` are pushed to your GitHub repository.
2.  **Create a new Web Service on Render**:
    *   Go to the Render Dashboard and click "New" > "Web Service".
    *   Connect your GitHub account and select your repository.
    *   Render will automatically detect the `render.yaml` file and configure the service for you.
3.  **Add Environment Variables**:
    *   Render will automatically add the `SECRET_KEY` environment variable for you.
    *   You will need to add a `DATABASE_URL` environment variable. You can get this from a Render PostgreSQL database.
4.  **Deploy**: Click "Create Web Service" to deploy your application.

## 4. Create a Render PostgreSQL Database

1.  **Create a new Database on Render**:
    *   Go to the Render Dashboard and click "New" > "PostgreSQL".
    *   Give your database a name and click "Create Database".
2.  **Get the Database URL**:
    *   Once the database is created, go to the "Info" tab and copy the "Internal Database URL".
3.  **Add the Database URL to your Web Service**:
    *   Go to your Web Service's "Environment" tab.
    *   Add a new environment variable with the key `DATABASE_URL` and the value you copied from the database.

## 5. Final Steps

*   **Run Migrations**: The `buildCommand` in your `render.yaml` file will automatically run migrations on every deploy.
*   **Create a Superuser**: You can create a superuser by running the following command in the Render shell:
    ```
    python manage.py createsuperuser
    ```

Your application should now be deployed and running on Render!
