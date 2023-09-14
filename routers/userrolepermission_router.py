from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schemas import UserRolePermissionUpdate
from database.database import SessionLocal
from models.models import UserRolePermission
from schemas.user_schemas import UserRolePermissionBase, UserRolePermissionCreate, UserRolePermissionUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/post")
def create_item(item: UserRolePermissionCreate, db: Session = Depends(get_db)):
   
    db_user_permission = UserRolePermission(**item.dict())
    try:    
        db.add(db_user_permission)
        db.commit()
        db.refresh(db_user_permission)
        return db_user_permission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    try:
        db_user_permission = db.query(UserRolePermission).filter(UserRolePermission.id == id).first()
        
        if db_user_permission is None:
            raise HTTPException(status_code=404, detail="User permission not found")
        
        return db_user_permission
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}/")
def update_item(id: int, item: UserRolePermissionUpdate, db: Session = Depends(get_db)):
    try:
        db_user_permission = db.query(UserRolePermission).filter(UserRolePermission.id == id).first()
        
        if db_user_permission is None:
            raise HTTPException(status_code=404, detail="User permission not found")
        
        for key, value in item.dict().items():
            setattr(db_user_permission, key, value)
        
        db.commit()
        db.refresh(db_user_permission)
        
        return db_user_permission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    try:
       
        db_user_permission = db.query(UserRolePermission).filter(UserRolePermission.id == id).first()
        
        if db_user_permission is None:
            raise HTTPException(status_code=404, detail="User permission not found")
        
        db.delete(db_user_permission)
        db.commit()
    
        return {"message": "User permission deleted successfully"}
    except Exception as e:
        
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

