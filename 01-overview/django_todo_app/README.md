# Django TODO Application

A modern, feature-rich TODO application built with Django, featuring a beautiful UI with light/dark mode support and comprehensive test coverage.

![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Tests](https://img.shields.io/badge/Tests-22%20passed-success.svg)

## Features

✨ **Core Functionality**

- Create, read, update, and delete TODO items
- Assign due dates to tasks
- Mark tasks as resolved/active
- Filter tasks by status (All, Active, Resolved)

🎨 **Modern UI**

- Beautiful, responsive design with Inter font
- Light and Dark mode with persistent theme preference
- Smooth animations and hover effects
- Card-based layout with status badges

🧪 **Robust Testing**

- 22 comprehensive tests covering models, views, and URLs
- 100% test coverage for core functionality

## Quick Start

### Prerequisites

- Python 3.13+ (developed with 3.13.2, compatible with 3.10+)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/wanyingng/ai-dev-tools-zoomcamp-2025.git
   cd ai-dev-tools-zoomcamp-2025\01-overview\django_todo_app
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install django
   ```

3. **Run migrations**

   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser (optional)**

   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Start the development server**

   ```bash
   uv run python manage.py runserver
   ```

6. **Open your browser**
   - Application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
django_todo_app/
├── todo_project/            # Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── todos/                   # Main TODO app
│   ├── migrations/          # Database migrations
│   ├── templates/todos/     # HTML templates
│   │   ├── base.html        # Base template with CSS & theme toggle
│   │   ├── home.html        # TODO list view
│   │   ├── todo_form.html   # Create/Edit form
│   │   └── todo_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py
│   ├── models.py            # TodoItem model
│   ├── tests.py             # Comprehensive test suite
│   ├── urls.py              # App URL patterns
│   └── views.py             # CRUD views
│
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database (created after migrations)
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Dependency lock file
└── README.md                # This file
```

## Usage

### Creating a TODO

1. Click the "+ New Task" button
2. Fill in the title (required), description (optional), and due date (optional)
3. Click "Save Task"

### Editing a TODO

1. Click the edit icon on any task
2. Modify the fields as needed
3. Check "Mark as Resolved" to complete the task
4. Click "Save Task"

### Filtering TODOs

Use the filter buttons at the top:

- **All**: Show all tasks
- **Active**: Show only unresolved tasks
- **Resolved**: Show only completed tasks

### Dark Mode

Click the sun/moon icon in the header to toggle between light and dark themes. Your preference is saved automatically.

## Running Tests

Run the full test suite:

```bash
uv run python manage.py test
```

Run specific test classes:

```bash
uv run python manage.py test todos.tests.TodoItemModelTests
uv run python manage.py test todos.tests.TodoListViewTests
```

Run with verbose output:

```bash
uv run python manage.py test -v 2
```

## Tech Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Typography**: Inter (Google Fonts)
- **Testing**: Django TestCase

## Development

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all classes and methods

### Adding New Features

1. Create a new branch
2. Write tests first (TDD approach)
3. Implement the feature
4. Ensure all tests pass
5. Submit a pull request

---

Vibe coded with ❤️ by Quinn Ng using Google Antigravity
