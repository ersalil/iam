from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import Permission, UserRole, UserRolePermission
from schemas.userrole_schemas import UserRoleBase, UserRoleCreate
from database.database import get_db
from uid import unique_id

router = APIRouter()

@router.get('/{id}/')
def get_role(id: int, db: Session = Depends(get_db)):
    result = db.query(UserRole).filter(UserRole.roleid == id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="UserRole not found")

    
    permissions = db.query(Permission).join(UserRolePermission).filter(UserRolePermission.user_role_id == id).all()
    result.permissions = permissions  
    
    return result

@router.post("/")
def create_item(item: UserRoleCreate, db: Session = Depends(get_db)):
    if type(item) != dict:
        item = item.dict()
        
    items = item
    print("1. ",items,item)    
    permission_id = items.pop('permission_id')
    print("2. ",items,item)    
    items['roleid'] = unique_id()
    print("3. ",items,item)    
    db_userrole = UserRole(**items)
    db.add(db_userrole)
    db.commit()
    db.refresh(db_userrole)
   
    
    print(item)

    if permission_id: 
        for per_id in permission_id:
            # permission = db.query(Permission).filter(Permission.permissionid == permission_id).first()
            # if permission:
            db_user_role_permission = UserRolePermission(roleid=db_userrole.roleid, permissionid=per_id)
            db.add(db_user_role_permission)
            db.commit()
    db_userrole=db_userrole.to_dict(db_userrole)
    db_userrole['permission_id']=permission_id
    return db_userrole

@router.put("/{id}/")
def update_item(id: int, item: UserRoleBase, db: Session = Depends(get_db)):
    db_userrole = db.query(UserRole).filter(UserRole.roleid == id).first()
    if db_userrole is None:
        raise HTTPException(status_code=404, detail="UserRole not found")
    
    for key, value in item.dict().items():
        setattr(db_userrole, key, value)

    db.commit()

    if item.permission_id:  
        db.query(UserRolePermission).filter(UserRolePermission.user_role_id == id).delete()
        for permission_id in item.permission_ids:
            permission = db.query(Permission).filter(Permission.permissionid == permission_id).first()
            if permission:
                db_user_role_permission = UserRolePermission(user_role_id=db_userrole.roleid, permission_id=permission_id)
                db.add(db_user_role_permission)
                db.commit()

    db.refresh(db_userrole)
    return db_userrole

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_userrole = db.query(UserRole).filter(UserRole.roleid == id).first()
    if db_userrole is None:
        raise HTTPException(status_code=404, detail="UserRole not found")
    
    db.query(UserRolePermission).filter(UserRolePermission.user_role_id == id).delete()

    db.delete(db_userrole)
    db.commit()
    return {"status": "UserRole deleted successfully"}
