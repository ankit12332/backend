from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..models.models import User, UserRole
from ..schemas.schemas import Note, NoteCreate, NoteUpdate
from ..crud import crud_note

router = APIRouter()

@router.get("/", response_model=List[Note])
def read_notes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    notes = crud_note.get_notes_by_organization(db, organization_id=current_user.organization_id, skip=skip, limit=limit)
    return notes

@router.post("/", response_model=Note)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud_note.create_note(db=db, note=note, user_id=current_user.id, organization_id=current_user.organization_id)

@router.get("/{note_id}", response_model=Note)
def read_note(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_note = crud_note.get_note(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    if db_note.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db_note

@router.put("/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    note: NoteUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_note = crud_note.get_note(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    if db_note.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud_note.update_note(db=db, note_id=note_id, note_update=note)

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_note = crud_note.get_note(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    if db_note.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Only ADMIN can delete notes
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admin can delete notes")
    
    success = crud_note.delete_note(db=db, note_id=note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}