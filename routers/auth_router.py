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
# from auditlog_router import create_item as audit_create
from services.user_auth import save_password
from fastapi.security import OAuth2PasswordRequestForm
from uid import unique_id
from database.database import get_db

router = APIRouter()
        
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if type(user) != dict:
            user = user.dict()
    if db.query(User).filter(
        (User.username == user['username']) | (User.email == user['email'])
    ).first():
        raise HTTPException(status_code=400, detail="Please login, User already exists")
    user_data = user
    password = user_data.pop('password')
    user_data['userid'] = unique_id()
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    save_password(user_data,password,db)
    create_audit_log(user_data, 'Signup', db)
    return create_access_token(db_user,expires_delta=None, db=db)

@router.post("/login")
def user_login(item: LoginBase, db: Session = Depends(get_db)):
    print(item)
    db_user = db.query(User).filter(User.username == item.username).first()
    print(db_user)
    if not db_user:
        print("login")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    db_auth = db.query(UserAuthentication).filter(
        UserAuthentication.userid == db_user.userid).filter(
        UserAuthentication.methodid == '9d1886ed-8eb7-4cba-8c5d-60c9d7149104'
    ).first()

    if not db_auth or not verify_password(item.password, db_auth.value):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return create_access_token(db_user, db=db)

@router.get("/logout", response_model=dict)
def logout(current_user: UserToken = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=400, detail="User not authenticated")

    if delete_session(db=db, id=current_user.userid):
        return {"detail": "Logged out successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to log out")