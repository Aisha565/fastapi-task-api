# FastAPI Task Management API

A containerized REST API built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **JWT authentication** for managing user-specific tasks.

The project was developed incrementally from a basic FastAPI application into a modular backend with authentication, database persistence, Docker, Docker Compose, and PostgreSQL.

## Features

* User registration
* Secure password hashing with bcrypt
* JWT-based authentication
* Protected task endpoints
* User-specific task access
* Full task CRUD operations
* Task filtering by completion status
* Task limit parameter
* Pydantic request/response validation
* SQLAlchemy ORM
* PostgreSQL database
* PostgreSQL persistent volume
* Docker containerization
* Docker Compose orchestration
* PostgreSQL healthcheck
* Non-root Docker container user
* Interactive Swagger API documentation
* Postman API testing

## Tech Stack

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| Python 3.12    | Programming language          |
| FastAPI        | REST API framework            |
| Pydantic       | Request/response validation   |
| SQLAlchemy     | ORM and database access       |
| PostgreSQL 16  | Relational database           |
| Psycopg        | PostgreSQL driver             |
| JWT            | Authentication                |
| bcrypt         | Password hashing              |
| Docker         | Application containerization  |
| Docker Compose | Multi-container orchestration |
| Postman        | API testing                   |
| Pytest         | Testing                       |

## Project Structure

```text
task-api/
│
├── main.py                 # FastAPI application and application-level routes
├── database.py             # Database engine, sessions, and ORM models
├── schemas.py              # Pydantic request/response schemas
├── security.py             # Password hashing and JWT utilities
│
├── routers/
│   ├── auth.py             # Login and authentication
│   ├── tasks.py            # Task CRUD and protected task routes
│   └── users.py            # User registration
│
├── tests/                  # Automated tests
│
├── Dockerfile              # FastAPI application image
├── compose.yaml            # FastAPI + PostgreSQL services
├── .dockerignore           # Files excluded from Docker build context
├── .gitignore              # Files excluded from Git
├── requirements.txt        # Python dependencies
└── README.md
```

## Architecture

The application runs as two Docker Compose services:

```text
                    Client
                      │
                      ▼
              FastAPI Application
                task-api-container
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
     JWT Authentication      PostgreSQL
                              task-api-db
                                  │
                                  ▼
                         Persistent Volume
                           postgres_data
```

### Request flow

```text
Client
  │
  ▼
FastAPI endpoint
  │
  ├── Pydantic validation
  │
  ├── JWT authentication
  │
  ├── SQLAlchemy
  │
  ▼
PostgreSQL
```

## Prerequisites

Install the following before running the project:

* Python 3.12+
* Git
* Docker Desktop
* Postman (optional, for API testing)

Docker Desktop must be running before starting the application with Docker Compose.

## Running with Docker

### 1. Clone the repository

```bash
git clone https://github.com/Aisha565/fastapi-task-api.git
cd fastapi-task-api
```

### 2. Create the environment file

Create a file named `.env` in the project root:

```env
POSTGRES_USER=taskapi
POSTGRES_PASSWORD=devpassword
POSTGRES_DB=tasks
```

> `.env` is intentionally excluded from Git because it contains environment-specific configuration and may contain secrets in real deployments.

### 3. Build and start the services

```bash
docker compose up -d --build
```

This starts:

* FastAPI application
* PostgreSQL database

The API waits for PostgreSQL to become healthy before starting.

### 4. Check running containers

```bash
docker compose ps
```

Expected services:

```text
task-api-container
task-api-db
```

The PostgreSQL service should show a healthy status.

### 5. Open the API

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected health response:

```json
{
  "status": "healthy",
  "message": "Task API is running"
}
```

## API Endpoints

### Users

| Method | Endpoint | Authentication | Purpose             |
| ------ | -------- | -------------- | ------------------- |
| POST   | `/users` | No             | Register a new user |

### Authentication

| Method | Endpoint | Authentication | Purpose                          |
| ------ | -------- | -------------- | -------------------------------- |
| POST   | `/login` | No             | Authenticate user and return JWT |

### Tasks

| Method | Endpoint           | Authentication | Purpose                   |
| ------ | ------------------ | -------------- | ------------------------- |
| GET    | `/tasks`           | JWT            | List current user's tasks |
| POST   | `/tasks`           | JWT            | Create a task             |
| GET    | `/tasks/{task_id}` | JWT            | Get a specific task       |
| PUT    | `/tasks/{task_id}` | JWT            | Update a task             |
| DELETE | `/tasks/{task_id}` | JWT            | Delete a task             |

### System

| Method | Endpoint  | Authentication | Purpose                  |
| ------ | --------- | -------------- | ------------------------ |
| GET    | `/`       | No             | API root                 |
| GET    | `/health` | No             | Application health check |

## Authentication Flow

The API uses JWT-based authentication.

```text
Register
   │
   ▼
POST /users
   │
   ▼
Password is hashed
   │
   ▼
User stored in PostgreSQL
   │
   ▼
POST /login
   │
   ▼
JWT access token
   │
   ▼
Authorization: Bearer <token>
   │
   ▼
Protected task endpoints
```

Passwords are never stored as plain text. The application stores bcrypt password hashes.

## Example Requests

### Register

**POST `/users`**

```json
{
  "email": "user@example.com",
  "password": "12345678"
}
```

### Login

**POST `/login`**

The login endpoint uses form data:

```text
username=user@example.com
password=12345678
```

The response contains an access token.

Use the token in protected requests:

```text
Authorization: Bearer <access_token>
```

### Create a task

**POST `/tasks`**

```json
{
  "title": "Complete Docker assignment",
  "description": "Finish containerization and documentation",
  "priority": 1,
  "due_date": ""
}
```

### List tasks

**GET `/tasks`**

Example response:

```json
{
  "limit": 10,
  "done": false,
  "tasks": []
}
```

## Database

The application uses **PostgreSQL 16** when running through Docker Compose.

The database connection is configured using environment variables:

```text
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

The FastAPI container connects to PostgreSQL through the Compose service name:

```text
db:5432
```

A named Docker volume is used for database persistence:

```text
postgres_data
```

This means PostgreSQL data remains available when the containers are stopped and recreated.

## Docker Configuration

The Docker image is built using:

```text
python:3.12-slim
```

The application:

1. Copies dependency definitions
2. Installs Python dependencies
3. Copies the application source code
4. Creates a dedicated non-root user
5. Runs FastAPI as that user

The container runs Uvicorn on:

```text
0.0.0.0:8000
```

The application is exposed locally through:

```text
127.0.0.1:8000
```

## PostgreSQL Healthcheck

Docker Compose uses PostgreSQL's `pg_isready` command to check database readiness.

The FastAPI service depends on the database health status before starting.

This prevents the API from attempting to connect before PostgreSQL is ready.

## Testing

The API was tested through:

* Swagger UI
* Postman
* Docker container health checks
* PostgreSQL connection
* JWT authentication flow
* User-specific task access

Example verification flow:

```text
Register user
     ↓
Login
     ↓
Receive JWT
     ↓
Create task
     ↓
Get tasks
     ↓
Verify task is stored in PostgreSQL
```

## Useful Docker Commands

Start the application:

```bash
docker compose up -d --build
```

View running services:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs task-api
```

View database logs:

```bash
docker compose logs db
```

Stop the services:

```bash
docker compose down
```

Stop services without removing the PostgreSQL volume:

```bash
docker compose down
```

> Avoid `docker compose down -v` unless you intentionally want to delete the PostgreSQL volume and its stored data.

## Local Development Without Docker

A local Python environment can also be used for development.

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

For local development, PostgreSQL must be available and the required environment variables must be configured.

Run the application:

```powershell
uvicorn main:app --reload
```

## Security Practices

The project follows several basic backend security practices:

* Passwords are hashed using bcrypt.
* Passwords are not stored in plain text.
* Protected task routes require JWT authentication.
* Users can access only their own tasks.
* `.env` is excluded from Git.
* Database files are excluded from the Docker build context.
* The Docker application runs as a non-root user.
* Database credentials are supplied through environment variables rather than hardcoded in the application.

For production deployment, additional security measures would be required, including secure secret management, HTTPS, stronger production credentials, token configuration, database migrations, and appropriate infrastructure controls.

## Key Learning Outcomes

This project helped develop practical understanding of:

* REST API design
* FastAPI routing
* Pydantic validation
* Dependency injection
* SQLAlchemy ORM
* PostgreSQL
* JWT authentication
* Password hashing
* Docker images and containers
* Docker Compose
* Environment variables
* Container networking
* Persistent Docker volumes
* Database healthchecks
* API testing with Postman
* Git and GitHub collaboration workflow

## Future Improvements

Potential next improvements include:

* Alembic database migrations
* More comprehensive automated test coverage
* Multi-stage Docker builds
* Production-grade secret management
* API rate limiting
* Structured logging
* CI/CD with GitHub Actions
* PostgreSQL connection pooling configuration
* Production deployment

## Author

**Ayesha Abbas**

BS Computer Science

GitHub: `https://github.com/Aisha565`
