
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.models import UserRolePermission
from ..schemas.schemas import UserRolePermissionBase, UserRolePermissionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/userrolepermission/")
def create_item(item: UserRolePermissionCreate, db: Session = Depends(get_db)):
    # Add logic to create an item
    pass

@router.get("/userrolepermission/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    # Add logic to read an item by its ID
    pass

@router.put("/userrolepermission/{id}/")
def update_item(id: int, item: UserRolePermissionBase, db: Session = Depends(get_db)):
    # Add logic to update an item by its ID
    pass

@router.delete("/userrolepermission/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    # Add logic to delete an item by its ID
    pass
