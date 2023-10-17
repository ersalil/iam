
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from database.database import SessionLocal
from schemas.user_schemas import PermissionBase, PermissionCreate
from models.models import Permission
from database.database import get_db
from uid import unique_id

router = APIRouter()

@router.post("/")
def create_item(item: PermissionCreate, db: Session = Depends(get_db)):
    try:
        if type(item) != dict:
            item = item.dict()
        item['permissionid'] = unique_id()
        db_permission = Permission(**item)
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


@router.post("/bulk/")
def create_bulk_permissions(items: list[PermissionCreate], db: Session = Depends(get_db)):
    try:
        
        created_permissions = []

        for item in items:
            print(item)
            if type(item) != dict:
                item = item.dict()
            item['permissionid'] = unique_id()
            db_permission = Permission(**item)
            db.add(db_permission)
            db.commit()
            db.refresh(db_permission)
            print(created_permissions)
            created_permissions.append(db_permission.to_dict(db_permission))

        return created_permissions

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
def get_clienttype_id(request: Request) -> int:
    clienttypeid = request.query_params.get('clienttypeid')
    if clienttypeid is None:
        raise HTTPException(status_code=400, detail="Client Type ID is required")
    return int(clienttypeid)


