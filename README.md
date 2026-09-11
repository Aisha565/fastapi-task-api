# FastAPI Task Management API

A REST API built with **FastAPI** for managing tasks with **SQLite**, **SQLAlchemy**, and **JWT-based authentication**.

## Features

* User registration
* Secure password hashing with bcrypt
* User login with JWT authentication
* Protected task endpoints
* Create, read, update, partially update, and delete tasks
* User-specific task ownership
* SQLite database with SQLAlchemy ORM
* Request and response validation with Pydantic
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

## Project Structure

```text
task-api/
│
├── main.py
├── database.py
├── schemas.py
├── security.py
├── requirements.txt
│
└── routers/
    ├── __init__.py
    ├── tasks.py
    ├── users.py
    └── auth.py
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
* Protected endpoints verify the JWT before allowing access.
* Task ownership is checked using the authenticated user's ID.

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
* User authorization and resource ownership
* API testing with Swagger UI
