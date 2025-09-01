# Notes & Todos API - FastAPI Backend

A full-stack application backend built with FastAPI, PostgreSQL, and JWT authentication featuring role-based access control (RBAC) and organization-based data sharing.

## Features

- **JWT Authentication**: Secure user signup and login
- **Role-Based Access Control (RBAC)**: Admin and Member roles with different permissions
- **Organization-Based Data Sharing**: Users within the same organization share notes and todos
- **CRUD Operations**: Full Create, Read, Update, Delete operations for Notes and Todos
- **Database Migrations**: Alembic for database schema management
- **Automated Tests**: Comprehensive test coverage for auth, RBAC, and data access

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Alembic**: Database migration tool
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation using Python type annotations
- **Pytest**: Testing framework

## Database Schema

### Tables

1. **organizations**: Organization information
2. **users**: User accounts with organization association
3. **notes**: Shared notes within organizations
4. **todos**: Shared todos within organizations

### Relationships

- Users belong to Organizations (many-to-one)
- Notes belong to Organizations (many-to-one)
- Todos belong to Organizations (many-to-one)
- Users can create multiple Notes and Todos

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- Git

### 1. Clone and Setup Project

```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Make sure PostgreSQL is running and create a database named `assignment` with user `ankit` and password `9658523363`.

Or update the database credentials in `.env` file:

```bash
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run Database Migrations

```bash
# Initialize Alembic (already done)
# alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 6. Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### 7. API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/signup` - User registration with organization creation
- `POST /auth/login` - User login (returns JWT token)

### Notes

- `GET /notes/` - Get all notes for user's organization
- `POST /notes/` - Create new note
- `GET /notes/{id}` - Get specific note
- `PUT /notes/{id}` - Update note
- `DELETE /notes/{id}` - Delete note (Admin only)

### Todos

- `GET /todos/` - Get all todos for user's organization
- `POST /todos/` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo (Admin only)

## RBAC Implementation

### Roles

1. **ADMIN**: Can create, read, update, and delete notes/todos
2. **MEMBER**: Can create, read, and update notes/todos (cannot delete)

### Organization-Based Access

- Users can only access data from their own organization
- All CRUD operations are scoped to the user's organization
- Data sharing is automatic within the same organization

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest app/tests/test_auth.py

# Run with coverage
pytest --cov=app
```

## Project Structure

```
backend/
├── app/
│   ├── core/           # Core functionality (config, database, security)
│   ├── crud/           # Database operations
│   ├── models/         # SQLAlchemy models
│   ├── routers/        # FastAPI routers
│   ├── schemas/        # Pydantic schemas
│   ├── tests/          # Test files
│   └── main.py         # FastAPI application
├── alembic/            # Database migrations
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── README.md          # This file
```

## Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with configurable expiration
- **Role-Based Authorization**: Different permissions for Admin/Member roles
- **Organization Isolation**: Users can only access their organization's data
- **Input Validation**: Pydantic schemas for request/response validation

## Environment Variables

```bash
DATABASE_URL=postgresql://ankit:9658523363@localhost:5432/assignment
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Example Usage

### 1. Register a new user

```bash
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword",
       "organization_name": "Acme Corp"
     }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=securepassword"
```

### 3. Create a note (with JWT token)

```bash
curl -X POST "http://localhost:8000/notes/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "title": "Meeting Notes",
       "content": "Discussed project timeline and deliverables"
     }'
```

## Development Notes

- The application uses SQLAlchemy's declarative base for ORM
- JWT tokens expire after 30 minutes (configurable)
- CORS is enabled for frontend integration
- Database migrations are handled by Alembic
- All endpoints require authentication except signup/login
- Organization-based data isolation is enforced at the database query level

## Troubleshooting

1. **Database connection issues**: Check PostgreSQL is running and credentials in `.env`
2. **Migration errors**: Ensure database exists and user has proper permissions
3. **JWT token errors**: Check SECRET_KEY in environment variables
4. **CORS issues**: Update allowed origins in `main.py`

For more detailed API documentation, visit `http://localhost:8000/docs` after starting the server.