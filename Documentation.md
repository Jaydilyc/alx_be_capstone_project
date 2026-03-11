# Task Management API

A RESTful backend API for managing tasks and projects, built with **Django** and **Django REST Framework (DRF)**.  
This API allows users to create projects, manage tasks, track task completion, and organize tasks by priority, status, and project.

The system includes secure **JWT authentication**, **task filtering**, **task status logic**, and **ownership-based permissions** to ensure that users can only manage their own resources.

---

# Project Overview

The Task Management API enables users to organize their work efficiently by providing endpoints to:

- Register and authenticate users
- Create and manage projects
- Create and manage tasks
- Mark tasks as completed or incomplete
- Filter and sort tasks
- Enforce ownership permissions
- Run automated API tests

This project simulates a **production-ready backend service** and demonstrates core backend development skills including:

- REST API design
- database modeling
- authentication
- permissions
- testing
- documentation

---

# Technology Stack

| Technology | Purpose |
|-----------|--------|
| Python | Programming language |
| Django | Backend web framework |
| Django REST Framework | API development |
| SimpleJWT | Token authentication |
| SQLite | Development database |
| Git & GitHub | Version control |
| Curl / Postman | API testing |

---

# Project Architecture

The project follows a **modular Django app architecture**:

# File Directory Structure

task_management_api/
│
├── users/
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
├── projects/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
├── tasks/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
├── task_management_api/
│ ├── settings.py
│ ├── urls.py
│
└── manage.py



### App Responsibilities

**users**
- registration
- authentication
- profile management

**projects**
- project CRUD operations

**tasks**
- task CRUD operations
- task status management
- filtering and sorting

---

# Installation Guide

## 1 Clone the repository

```bash
git clone https://github.com/Jaydilyc/alx_be_capstone_project.git
cd alx_be_capstone_project


2 Create virtual environment
python -m venv venv

Activate environment:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3 Install dependencies
pip install -r requirements.txt
4 Run migrations
python manage.py makemigrations
python manage.py migrate
5 Start the development server
python manage.py runserver

Server runs at:

http://127.0.0.1:8000/
Authentication

The API uses JWT token authentication.

Users must authenticate before accessing project or task endpoints.

Register User
POST /api/register/

Example request:

{
  "username": "john",
  "email": "john@example.com",
  "password": "StrongPassword123"
}
Login User
POST /api/token/

Example request:

{
  "username": "john",
  "password": "StrongPassword123"
}

Response:

{
  "refresh": "token",
  "access": "token"
}
Get User Profile
GET /api/profile/

Authorization header:

Authorization: Bearer <access_token>


Project API Endpoints
Method	Endpoint	Description
POST	/api/projects/	Create project
GET	/api/projects/	List user projects
GET	/api/projects/{id}/	Retrieve project
PUT	/api/projects/{id}/	Update project
DELETE	/api/projects/{id}/	Delete project
Task API Endpoints
Method	Endpoint	Description
POST	/api/tasks/	Create task
GET	/api/tasks/	List tasks
GET	/api/tasks/{id}/	Retrieve task
PUT	/api/tasks/{id}/	Update task
DELETE	/api/tasks/{id}/	Delete task
Task Status Endpoints

Tasks can be marked as completed or reverted to pending.

Method	Endpoint	Description
PATCH	/api/tasks/{id}/complete/	Mark task completed
PATCH	/api/tasks/{id}/incomplete/	Mark task pending

When a task is marked completed, a completion timestamp is recorded.

Filtering and Sorting

Tasks can be filtered using query parameters.

Filter by Status
/api/tasks/?status=pending
/api/tasks/?status=completed
Filter by Priority
/api/tasks/?priority=high
Filter by Project
/api/tasks/?project=1
Sorting
/api/tasks/?ordering=due_date
/api/tasks/?ordering=priority
Permissions

The API enforces object-level ownership permissions.

Rules:

users can only access their own projects

users can only access their own tasks

users cannot update or delete another user’s data

Permissions are enforced using:

IsAuthenticated

object-level ownership checks

Running Tests

Run the automated test suite:

python manage.py test

Tests include:

authentication tests

project API tests

task API tests

task status logic tests

filtering tests

permission tests

Example Curl Requests
Create Project
curl -X POST http://127.0.0.1:8000/api/projects/ \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{"name":"Backend Capstone","description":"Project API"}'
Create Task
curl -X POST http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Build serializers","priority":"high"}'
Future Improvements

Potential enhancements include:

Task categories

Recurring tasks

Email reminders

Task collaboration

Pagination

API rate limiting

Swagger API documentation

Author

Oladipo Adeeko

GitHub:
https://github.com/Jaydilyc

ALX Backend Capstone Project
