import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db


# -------------------------
# Test Database
# -------------------------

TEST_DATABASE_URL = "sqlite:///./test_tasks.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(bind=test_engine)


# -------------------------
# Override Database
# -------------------------

def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# -------------------------
# Fresh Database for Each Test
# -------------------------

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


# -------------------------
# Helper Functions
# -------------------------

def register_user(email="user@example.com", password="password123"):
    return client.post(
        "/users",
        json={
            "email": email,
            "password": password
        }
    )


def login_user(email="user@example.com", password="password123"):
    response = client.post(
        "/login",
        data={
            "username": email,
            "password": password
        }
    )

    return response.json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


# -------------------------
# Test 1 - User Registration
# -------------------------

def test_register_user():
    response = register_user()

    assert response.status_code == 201
    assert response.json()["email"] == "user@example.com"


# -------------------------
# Test 2 - User Login
# -------------------------

def test_login_user():
    register_user()

    response = client.post(
        "/login",
        data={
            "username": "user@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# -------------------------
# Test 3 - Create Task
# -------------------------

def test_create_task():
    register_user()
    token = login_user()

    response = client.post(
        "/tasks",
        headers=auth_headers(token),
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "priority": 3,
            "due_date": ""
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"


# -------------------------
# Test 4 - Get Task
# -------------------------

def test_get_task():
    register_user()
    token = login_user()

    create_response = client.post(
        "/tasks",
        headers=auth_headers(token),
        json={
            "title": "Get Task",
            "description": "Testing GET",
            "priority": 2,
            "due_date": ""
        }
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["task"]["id"] == task_id


# -------------------------
# Test 5 - Update Task
# -------------------------

def test_update_task():
    register_user()
    token = login_user()

    create_response = client.post(
        "/tasks",
        headers=auth_headers(token),
        json={
            "title": "Old Title",
            "description": "Old description",
            "priority": 1,
            "due_date": ""
        }
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers=auth_headers(token),
        json={
            "title": "Updated Title",
            "description": "Updated description",
            "priority": 5,
            "due_date": ""
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["priority"] == 5


# -------------------------
# Test 6 - Delete Task
# -------------------------

def test_delete_task():
    register_user()
    token = login_user()

    create_response = client.post(
        "/tasks",
        headers=auth_headers(token),
        json={
            "title": "Delete Task",
            "description": "",
            "priority": 1,
            "due_date": ""
        }
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 204


# -------------------------
# Test 7 - Validation Error
# -------------------------

def test_task_validation():
    register_user()
    token = login_user()

    response = client.post(
        "/tasks",
        headers=auth_headers(token),
        json={
            "title": "",
            "description": "",
            "priority": 10,
            "due_date": ""
        }
    )

    assert response.status_code == 422


# -------------------------
# Test 8 - User Ownership
# -------------------------

def test_user_cannot_access_another_users_task():
    register_user(
        email="user_a@example.com",
        password="password123"
    )

    token_a = login_user(
        email="user_a@example.com",
        password="password123"
    )

    create_response = client.post(
        "/tasks",
        headers=auth_headers(token_a),
        json={
            "title": "User A Task",
            "description": "Private task",
            "priority": 1,
            "due_date": ""
        }
    )

    task_id = create_response.json()["id"]

    register_user(
        email="user_b@example.com",
        password="password123"
    )

    token_b = login_user(
        email="user_b@example.com",
        password="password123"
    )

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(token_b)
    )

    assert response.status_code == 404