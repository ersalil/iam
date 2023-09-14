from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import User, UserAuthentication, AuditLog
from schemas.user_schemas import UserBase, UserCreate, LoginBase, AuditLogCreate, AuditLogBase
from .usersession_router import create_item as create_session
from .usersession_router import delete_item as delete_session
from security.auth import jwt, get_current_user, verify_password, create_access_token, hash_password
from schemas.user_schemas import UserCreate, SignUp
from datetime import datetime
from .auditlog_router import create_item as audit_create
# from auditlog_router import create_item as audit_create
from .userauthentication_router import create_item as save_pass


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/signup")
def signup(user: SignUp, db: Session = Depends(get_db)):
    password = user.password
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    del user.password
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    get_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    data = {
        "userid": get_user.userid,
        "methodid": 3,
        "value": hash_password(password),
        "verificationstatus": True,
        "lastupdated": datetime.now()
    }
    print(data)
    save_pass(data, db)
    
    audit_data = {
        "userid": get_user.userid,
        "actiontype": "Signup",
        "timestamp": datetime.now()
    }
    audit_create(audit_data, db)

    jwt_data = create_access_token({"sub": get_user.email})

    session = {
        'userid': get_user.userid,
        'sessiontoken': jwt_data[0],
        'expirydate': jwt_data[1]
    }
    
    if not create_session(item=session, db=db):
        raise Exception("Could not create new session.")

    return {"access_token": jwt_data[0], "access_type": 'bearer'}

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
def read_item(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == id).first()
    print(db_user)   
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{id}/")
def update_item(id: int, item: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userid == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in item.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.userid == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"status": "User deleted successfully"}

@router.post("/login")
def user_login(item: LoginBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == item.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    db_auth = db.query(UserAuthentication).filter(
        UserAuthentication.userid == db_user.userid,
        UserAuthentication.methodid == 1  
    ).first()

    if not db_auth or not verify_password(item.password, db_auth.value):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})

    if not create_session(db, user_id=db_user.userid, token=access_token):
        raise Exception("Could not create new session.")

    return {"access_token": access_token, "access_type": 'bearer'}

@router.post("/logout", response_model=dict)
def logout(current_user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=400, detail="User not authenticated")

    if delete_session(db, user_id=current_user.userid):
        return {"detail": "Logged out successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to log out")
    
     
