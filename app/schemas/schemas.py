from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole

class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.MEMBER

class UserCreate(UserBase):
    password: str
    organization_id: int

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    organization_name: str

class User(UserBase):
    id: int
    organization_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Note(NoteBase):
    id: int
    created_by: int
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    completed: bool
    created_by: int
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def from_orm(cls, obj):
        # Convert integer completed field to boolean
        if hasattr(obj, 'completed'):
            obj.completed = bool(obj.completed)
        return super().from_orm(obj)

    class Config:
        from_attributes = True