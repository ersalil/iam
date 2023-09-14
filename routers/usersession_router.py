
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import UserSession
from schemas.user_schemas import UserSessionBase, UserSessionCreate, UserSession

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_item(item: UserSessionCreate, db: Session = Depends(get_db)):
    try:
        print(item)
        db_user_session = UserSession(**item)
        db.add(db_user_session)
        db.commit()
        db.refresh(db_user_session)
        
        return db_user_session
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
   
        
@router.get("/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    db_user_session = db.query(UserSession).filter(UserSession.id == id).first()
    
    if db_user_session is None:
        raise HTTPException(status_code=404, detail="User session not found")
    
    return db_user_session

@router.put("/{id}/")
def update_item(id: int, item: UserSessionBase, db: Session = Depends(get_db)):
    try:
        db_user_session = db.query(UserSession).filter(UserSession.id == id).first()
        
        if db_user_session is None:
            raise HTTPException(status_code=404, detail="User session not found")
        
        for key, value in item.dict().items():
            setattr(db_user_session, key, value)
        
        db.commit()
        db.refresh(db_user_session)
        
        return db_user_session
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    try:
        db_user_session = db.query(UserSession).filter(UserSession.id == id).first()
        
        if db_user_session is None:
            raise HTTPException(status_code=404, detail="User session not found")
        
        db.delete(db_user_session)
        
        db.commit()
        
        return {"message": "User session deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
