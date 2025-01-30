# Task Manager in Django

[Optional: Include a video thumbnail here if applicable]

This project implements a user-friendly task management system built with the Django framework. It allows users to create, assign, prioritize, and track tasks efficiently.

## Key Features

- **User Authentication**: Secure login system for enhanced data privacy.
- **Role-Based Access Control**: Differentiates between regular users and administrators, granting appropriate permissions.
- **Comprehensive Task Management**:
  - Create, edit, and delete tasks with ease.
  - Assign tasks to specific users for collaborative work.
  - Prioritize tasks effectively using a flexible priority system.
  - Track task statuses (e.g., To Do, In Progress, Completed) for progress monitoring.
  - Set due dates for timely task completion.
  - Provide detailed descriptions for enhanced task clarity.
- **Secure Data Handling**: Utilizes environment variables to store sensitive information outside the Git repository, ensuring security.
- **Database Flexibility**: Supports both SQLite (provided by default) and PostgreSQL for database management, offering flexibility in deployment.
- **User-Friendly Interface**: Leverages HTML, CSS, and Bootstrap templates for a visually appealing and intuitive user experience.
- **Streamlined Form Handling**: Employs Django-Crispy-Forms for efficient and user-friendly form creation.

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


