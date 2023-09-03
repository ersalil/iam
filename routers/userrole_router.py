from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import UserRole
from schemas.userrole_schemas import UserRoleBase, UserRoleCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/{id}/')
def get_role(id: int, db: Session = Depends(get_db)):
    result = db.query(UserRole).filter(UserRole.roleid == id).first()
    return result


@router.post("/")
def create_item(item: UserRoleCreate, db: Session = Depends(get_db)):
    db_userrole = UserRole(**item.dict())
    db.add(db_userrole)
    db.commit()
    db.refresh(db_userrole)
    return db_userrole

# @router.get("/{id}/")
# def read_item(id: int, db: Session = Depends(get_db)):
#     db_userrole = db.query(UserRole).filter(UserRole.RoleID == id).first()
#     if db_userrole is None:
#         raise HTTPException(status_code=404, detail="UserRole not found")
#     return db_userrole

@router.put("/{id}/")
def update_item(id: int, item: UserRoleBase, db: Session = Depends(get_db)):
    db_userrole = db.query(UserRole).filter(UserRole.RoleID == id).first()
    if db_userrole is None:
        raise HTTPException(status_code=404, detail="UserRole not found")
    
    for key, value in item.dict().items():
        setattr(db_userrole, key, value)

    db.commit()
    db.refresh(db_userrole)
    return db_userrole

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_userrole = db.query(UserRole).filter(UserRole.RoleID == id).first()
    if db_userrole is None:
        raise HTTPException(status_code=404, detail="UserRole not found")
    
    db.delete(db_userrole)
    db.commit()
    return {"status": "UserRole deleted successfully"}
