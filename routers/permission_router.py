
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.models import Permission
from ..schemas.schemas import PermissionBase, PermissionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/permission/")
def create_item(item: PermissionCreate, db: Session = Depends(get_db)):
    # Add logic to create an item
    pass

@router.get("/permission/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    # Add logic to read an item by its ID
    pass

@router.put("/permission/{id}/")
def update_item(id: int, item: PermissionBase, db: Session = Depends(get_db)):
    # Add logic to update an item by its ID
    pass

@router.delete("/permission/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    # Add logic to delete an item by its ID
    pass
