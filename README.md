# FastAPI Task Management API

A REST API built with **FastAPI** for managing tasks with **SQLite**, **SQLAlchemy**, and **JWT-based authentication**.

## Features

* User registration
* Secure password hashing with bcrypt
* User login with JWT authentication
* JWT access tokens with 24-hour expiration
* Protected task endpoints
* Create, read, update, partially update, and delete tasks
* User-specific task ownership
* SQLite database with SQLAlchemy ORM
* Request and response validation with Pydantic
* Input validation for task title, priority, and password
* Automated API testing with pytest
* Interactive API documentation with Swagger UI

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* bcrypt
* Uvicorn
* pytest

## Project Structure

```text
task-api/

│
├── main.py
├── database.py
├── schemas.py
├── security.py
├── requirements.txt
├── README.md
│
├── routers/
│   ├── __init__.py
│   ├── tasks.py
│   ├── users.py
│   └── auth.py
│
└── tests/
    ├── __init__.py
    └── test_api.py
```

## Setup

### 1. Create and activate virtual environment

```powershell
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

From the `task-api` folder:

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Authentication Flow

1. Register a user using `POST /users`
2. Login using `POST /login`
3. Receive a JWT access token
4. Click **Authorize** in Swagger UI
5. Enter the token
6. Access protected task endpoints

The token is sent using:

```text
Authorization: Bearer <access_token>
```

JWT access tokens expire after **24 hours**.

## Main Endpoints

### Users

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| POST   | `/users` | Register a new user |

### Authentication

| Method | Endpoint | Description                 |
| ------ | -------- | --------------------------- |
| POST   | `/login` | Login and receive JWT token |

### Tasks

| Method | Endpoint           | Description             |
| ------ | ------------------ | ----------------------- |
| GET    | `/tasks`           | Get tasks               |
| GET    | `/tasks/{task_id}` | Get a specific task     |
| POST   | `/tasks`           | Create a new task       |
| PUT    | `/tasks/{task_id}` | Update a task           |
| PATCH  | `/tasks/{task_id}` | Partially update a task |
| DELETE | `/tasks/{task_id}` | Delete a task           |

## Validation

The API uses **Pydantic** for request validation.

Examples:

* Task title cannot be empty.
* Task priority must be between **1 and 5**.
* User passwords must contain at least **8 characters**.
* Invalid input returns a `422 Unprocessable Entity` response.

## User Ownership

Each task is linked to the user who created it through `user_id`.

Protected task operations verify the authenticated user before accessing a task.

This means one user cannot access, update, or delete another user's tasks.

## Example Task

```json
{
  "title": "Learn FastAPI",
  "description": "Complete FastAPI project",
  "priority": 1,
  "due_date": ""
}
```

## Database

The project uses **SQLite** with **SQLAlchemy ORM**.

Two main database tables are used:

* `users` — stores user accounts and hashed passwords
* `tasks` — stores tasks and their associated user IDs

The database file `tasks.db` is created automatically when the application starts.

## Security

* Passwords are never stored as plain text.
* Passwords are hashed using bcrypt.
* JWT tokens are used for authentication.
* JWT tokens expire after 24 hours.
* Protected endpoints verify the JWT before allowing access.
* Task ownership is checked using the authenticated user's ID.

## Testing

The project includes **8 automated API tests** using pytest.

Tests cover:

* User registration
* User login
* Task creation
* Getting a task
* Updating a task
* Deleting a task
* Request validation
* Preventing one user from accessing another user's task

Run the tests with:

```powershell
pytest -v
```

Expected result:

```text
8 passed
```

## Learning Goals

This project was built to practice:

* FastAPI application structure
* REST API development
* CRUD operations
* Pydantic validation
* SQLAlchemy ORM
* SQLite database integration
* Dependency Injection
* Password hashing
* JWT authentication
* JWT expiration
* User authorization and resource ownership
* Automated API testing with pytest
* API testing with Swagger UI
