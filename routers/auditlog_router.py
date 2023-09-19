
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import AuditLog
from schemas.user_schemas import AuditLogBase, AuditLogCreate, SignUp
router = APIRouter()
from database.database import get_db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_item(item: AuditLogCreate, db: Session = Depends(get_db)):
    audit_log_entry = AuditLog(**item)
    db.add(audit_log_entry)
    db.commit()
    db.refresh(audit_log_entry)

    return audit_log_entry

@router.get("/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
   db_audit_log = db.query(AuditLog).filter(AuditLog.id == id).first()

   if db_audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log entry not found")

   return db_audit_log

@router.put("/{id}/")
def update_item(id: int, item: AuditLogBase, db: Session = Depends(get_db)):
    db_audit_log = db.query(AuditLog).filter(AuditLog.id == id).first()

    if db_audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log entry not found")

    for key, value in item.dict().items():
        setattr(db_audit_log, key, value)

    try:
        db.commit()
        db.refresh(db_audit_log)
        return db_audit_log
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_audit_log = db.query(AuditLog).filter(AuditLog.id == id).first()

    if db_audit_log is None:
        raise HTTPException(status_code=404, detail="Audit log entry not found")

    try:
        db.delete(db_audit_log)
        db.commit()
        return {"detail": "Audit log entry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))





