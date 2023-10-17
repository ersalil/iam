from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import User, UserAuthentication, AuditLog
from schemas.user_schemas import UserBase, UserCreate, LoginBase, AuditLogCreate, AuditLogBase, UserToken
from .usersession_router import create_item as create_session
from .usersession_router import delete_item as delete_session
from security.auth import jwt, get_current_user, verify_password, create_access_token, hash_password
from schemas.user_schemas import UserCreate, SignUp
from datetime import datetime
from services.user_auth import create_audit_log
#from auditlog_router import create_item as audit_create
from services.user_auth import save_password
from fastapi.security import OAuth2PasswordRequestForm
from uid import unique_id
from database.database import get_db

router = APIRouter()

@router.post("/")
def create_item(item: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**item.dict())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}/")
def read_item(id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == id).first()
    print(db_user)   
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{id}/")
def update_item(id: str, item: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in item.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{id}/")
def delete_item(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.userid == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"status": "User deleted successfully"}