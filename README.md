# Django Task Manager

A task management web application built with Python and Django. This project allows users to manage their daily tasks through a simple, responsive dashboard with user authentication and task tracking features.

## Features

- **User Authentication** — Register, log in, and log out securely.
- **Task Management (CRUD)** — Create, view, edit, and delete tasks.
- **Task Completion** — Mark tasks as completed or pending.
- **Search Tasks** — Find tasks by keywords.
- **Filter Tasks** — Filter tasks by completion status.
- **Pagination** — Navigate tasks across multiple pages.
- **User-Specific Tasks** — Users can access and manage only their own tasks.
- **Dashboard Statistics** — View task totals and completion progress.
- **Form Validation** — Validate task forms and display helpful error messages.
- **Automated Testing** — Test core application functionality.

## Tech Stack

| Technology | Purpose |

|---|---|
| Python | Backend programming |
| Django | Web framework |
| SQLite | Development database |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap | Responsive UI |
| Git & GitHub | Version control |

## Project Structure

```text
task-manager/
├── config/
│   ├── settings.py
│   └── urls.py
├── tasks/
│   ├── migrations/
│   ├── templates/
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── tasks/
│   │       ├── task_list.html
│   │       └── task_form.html
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/lipumehedi/django-task-manager.git
cd django-task-manager
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Add your own Django secret key:

```dotenv
SECRET_KEY=replace-with-your-own-secret-key
DEBUG=True
```

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key into `.env`. Never commit `.env` or expose your secret key publicly.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator (optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Start the development server

```bash
python manage.py runserver
```

Open the following URL in your browser:

http://127.0.0.1:8000/

## Running Tests

Run the task application tests with:

```bash
python manage.py test tasks
```

**Current test status:** 11 tests passed.

The tests cover authentication requirements, task creation, task ownership, editing, deletion, completion status, search, filtering, and pagination.

## Security

- Keep secret keys in environment variables.
- Exclude `.env`, virtual environments, and the local SQLite database from version control.
- Require authentication for task management.
- Restrict task operations to the task owner.
- Set `DEBUG=False` in production and configure production security settings before deployment.

## Learning Objectives

This project demonstrates practical experience with:

- Django models, views, templates, and URL routing.
- ModelForms and form validation.
- User authentication and authorization.
- Database migrations and ORM queries.
- Search, filtering, and pagination.
- Automated testing with Django's test framework.
- Git and GitHub workflow.

## Future Improvements

- Task priorities and categories.
- Due dates and deadline reminders.
- REST API using Django REST Framework.
- PostgreSQL database integration.
- Deployment to a cloud hosting platform.
- Additional test coverage and UI improvements.

## Author

***Mehedi Lipu**

- GitHub: [@lipumehedi](https://github.com/lipumehedi)

## License

This project is intended for learning and portfolio development. Add a formal open-source license if you decide to distribute it under specific terms.
