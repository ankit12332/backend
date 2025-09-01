from sqlalchemy.orm import Session
from ..models.models import Note, User
from ..schemas.schemas import NoteCreate, NoteUpdate

def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

def get_notes_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(Note).filter(Note.organization_id == organization_id).offset(skip).limit(limit).all()

def create_note(db: Session, note: NoteCreate, user_id: int, organization_id: int):
    db_note = Note(
        **note.dict(),
        created_by=user_id,
        organization_id=organization_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note_update: NoteUpdate):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        for key, value in note_update.dict(exclude_unset=True).items():
            setattr(db_note, key, value)
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False