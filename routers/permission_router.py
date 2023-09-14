
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from schemas.user_schemas import PermissionBase, PermissionCreate
from models.models import Permission

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_item(item: PermissionCreate, db: Session = Depends(get_db)):
    try:
        db_permission = Permission(**item.dict())
        
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        
        return db_permission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
   db_permission = db.query(Permission).filter(Permission.permissionid == id).first()
    
   if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    
   return db_permission


@router.put("/{id}/")
def update_item(item: PermissionBase, id: int, db: Session = Depends(get_db)):
    try:
        db_permission = db.query(Permission).filter(Permission.permissionid == id).first()
        
        if db_permission is None:
            raise HTTPException(status_code=404, detail="Permission not found")
        
        for key, value in item.dict().items():
            setattr(db_permission, key, value)
        
        db.commit()
        db.refresh(db_permission)
        
        return db_permission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    try:
        db_permission = db.query(Permission).filter(Permission.permissionid == id).first()
        
        if db_permission is None:
            raise HTTPException(status_code=404, detail="Permission not found")
        
        db.delete(db_permission)
        db.commit()
        
        return {"message": "Permission deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
