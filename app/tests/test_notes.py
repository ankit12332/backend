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

@pytest.fixture
def auth_headers(client):
    # Create user and get token
    client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "organization_name": "Test Org"
        },
    )
    
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_note(client, auth_headers):
    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test note"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note"

def test_read_notes(client, auth_headers):
    # Create a note first
    client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test note"},
        headers=auth_headers,
    )
    
    response = client.get("/notes/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Note"

def test_unauthorized_access(client):
    response = client.get("/notes/")
    assert response.status_code == 401