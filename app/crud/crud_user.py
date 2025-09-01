from sqlalchemy.orm import Session
from ..models.models import User, Organization
from ..schemas.schemas import UserCreate, UserSignup
from ..core.security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=user.role,
        organization_id=user.organization_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_with_organization(db: Session, user: UserSignup):
    # Create organization first
    db_org = Organization(name=user.organization_name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        organization_id=db_org.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user