from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import User
from schemas.user_schemas import UserBase, UserCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_item(item: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**item.dict())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()  # roll back any partial changes if an error occurred
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.UserID == id).first()
    print(db_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{id}/")
def update_item(id: int, item: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.UserID == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in item.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.UserID == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"status": "User deleted successfully"}
