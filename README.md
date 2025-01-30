# Task Manager in Django

[Optional: Include a video thumbnail here if applicable]

## Overview:
**This project is a robust task management system built with Django, designed for efficient task creation, assignment, prioritization, and tracking. It features secure user authentication, role-based access control, and a user-friendly interface powered by Bootstrap. Tasks can be categorized by status, assigned to users, and given due dates for better organization. The system ensures secure data handling using environment variables and supports both SQLite and PostgreSQL for flexible database management. With Django-Crispy-Forms, form handling is streamlined, enhancing usability.

## Getting Started

### Clone the Repository

```bash
gh repo clone phumlanimabophe/tasks-events-admin
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database (if using PostgreSQL)

# Setup currently no used
1. Install the psycopg2 library:
   ```bash
   pip install psycopg2
   ```
  # SQLite will not be ignored in commints

2. Configure database credentials in your environment variables.

### Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```
Enter your desired username and password.

Here is a superuser you can use (user already exists with original db):
- **User**: 123456789@gmail.com
- **Pass**: 123456789@gmail.com

### Start the Development Server

```bash
python manage.py runserver
```
Access the application in your web browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Usage

1. Log in to the application using the superuser credentials you created.
2. Create new tasks, assign them to users, set priorities and due dates, and track their progress.

## Bonus Features (Optional) - Completed

- **Dashboard**: Provides a high-level overview of task statistics, enabling better project management.
- **Calendar View**: Displays tasks with due dates on a calendar, allowing for easy scheduling and visual task prioritization.


