
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import AuthenticationMethod
from schemas.user_schemas import AuthenticationMethodBase
from uid import unique_id
from database.database import get_db

router = APIRouter()

@router.post("/")
def create_item(item: AuthenticationMethodBase, db: Session = Depends(get_db)):
    try:
        item = item.dict()
        item['methodid'] = unique_id()
        db_authmethod = AuthenticationMethod(**item)
        db.add(db_authmethod)
        db.commit()
        db.refresh(db_authmethod)
        return db_authmethod
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{authmethod_id}")
def get_item(authmethod_id: int, db: Session = Depends(get_db)):
    db_authmethod = db.query(AuthenticationMethod).filter(AuthenticationMethod.methodid == authmethod_id).first()
    if db_authmethod is None:
        raise HTTPException(status_code=404, detail="Authentication method not found")
    return db_authmethod
    
@router.put("/{authmethod_id}")
def update_item(authmethod_id: int, item: AuthenticationMethodBase, db: Session = Depends(get_db)):
    db_authmethod = db.query(AuthenticationMethod).filter(AuthenticationMethod.methodid == authmethod_id).first()

    if db_authmethod is None:
        raise HTTPException(status_code=404, detail="Authentication method not found")

    for key, value in item.dict().items():
        setattr(db_authmethod, key, value)

    try:
        db.commit()
        db.refresh(db_authmethod)
        return db_authmethod
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/{id}")
def delete_item(authmethod_id: int, db: Session = Depends(get_db)):
    db_authmethod = db.query(AuthenticationMethod).filter(AuthenticationMethod.methodid == authmethod_id).first()

    if db_authmethod is None:
        raise HTTPException(status_code=404, detail="Authentication method not found")

    try:
        db.delete(db_authmethod)
        db.commit()
        return {"detail": "Authentication method deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
