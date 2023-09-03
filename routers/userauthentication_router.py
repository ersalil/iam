
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.models import UserAuthentication
from ..schemas.schemas import UserAuthenticationBase, UserAuthenticationCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/userauthentication/")
def create_item(item: UserAuthenticationCreate, db: Session = Depends(get_db)):
    # Add logic to create an item
    pass

@router.get("/userauthentication/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    # Add logic to read an item by its ID
    pass

@router.put("/userauthentication/{id}/")
def update_item(id: int, item: UserAuthenticationBase, db: Session = Depends(get_db)):
    # Add logic to update an item by its ID
    pass

@router.delete("/userauthentication/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    # Add logic to delete an item by its ID
    pass
