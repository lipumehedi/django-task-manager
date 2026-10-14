
# Django Task Manager

A task management web application built with Python and Django.

## Features

- Create tasks with titles and descriptions
- View all tasks
- Mark tasks as completed or pending
- Delete tasks
- Search tasks by title
- Filter tasks by completion status
- Store tasks in a database

## Tech Stack

- Python
- Django
- SQLite
- HTML
- Bootstrap 5

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd task-manager
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create your local .env file

Generate a Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Create `.env` in the project root:

```text
DJANGO_SECRET_KEY=your-generated-secret-key
```

Replace the example value with your generated key.

### 5. Initialize the database

```bash
python manage.py migrate
```

### 6. Run the application

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Security

- Never commit `.env` or real secrets.
- The local SQLite database is excluded from Git.
- Configure a separate production secret key and production settings before deployment.
