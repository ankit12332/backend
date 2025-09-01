import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..core.database import get_db, Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(setup_database):
    return TestClient(app)

def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "organization_name": "Test Org"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_login(client):
    # First signup
    client.post(
        "/auth/signup",
        json={
            "username": "testuser2",
            "email": "test2@example.com", 
            "password": "testpassword",
            "organization_name": "Test Org 2"
        },
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        data={"username": "testuser2", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    # First signup
    client.post(
        "/auth/signup",
        json={
            "username": "testuser3",
            "email": "test3@example.com",
            "password": "testpassword",
            "organization_name": "Test Org 3"
        },
    )
    
    # Try login with wrong password
    response = client.post(
        "/auth/login",
        data={"username": "testuser3", "password": "wrongpassword"},
    )
    assert response.status_code == 401