from sqlalchemy.orm import Session
from ..models.models import Todo
from ..schemas.schemas import TodoCreate, TodoUpdate

def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(Todo).filter(Todo.organization_id == organization_id).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: TodoCreate, user_id: int, organization_id: int):
    db_todo = Todo(
        **todo.dict(),
        created_by=user_id,
        organization_id=organization_id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        update_data = todo_update.dict(exclude_unset=True)
        if 'completed' in update_data:
            update_data['completed'] = 1 if update_data['completed'] else 0
        
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False