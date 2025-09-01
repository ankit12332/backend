from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..models.models import User, UserRole
from ..schemas.schemas import Todo, TodoCreate, TodoUpdate
from ..crud import crud_todo

router = APIRouter()

@router.get("/", response_model=List[Todo])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    todos = crud_todo.get_todos_by_organization(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return todos

@router.post("/", response_model=Todo)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud_todo.create_todo(db=db, todo=todo, user_id=current_user.id, organization_id=current_user.organization_id)

@router.get("/{todo_id}", response_model=Todo)
def read_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_todo = crud_todo.get_todo(db, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db_todo

@router.put("/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_todo = crud_todo.get_todo(db, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud_todo.update_todo(db=db, todo_id=todo_id, todo_update=todo)

@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_todo = crud_todo.get_todo(db, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Only ADMIN can delete todos
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admin can delete todos")
    
    success = crud_todo.delete_todo(db=db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}