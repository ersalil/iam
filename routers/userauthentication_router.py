
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import UserAuthentication
from schemas.user_schemas import UserAuthenticationBase, UserAuthenticationCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_item(item: UserAuthenticationCreate, db: Session = Depends(get_db)):
    existing_auth_entry = db.query(UserAuthentication).filter(
    UserAuthentication.userid == item['userid'],
    UserAuthentication.methodid == item['methodid']
).first()
    if existing_auth_entry:
        raise HTTPException(status_code=400, detail="User authentication entry already exists")

    db_auth_entry = UserAuthentication(**item)

    db.add(db_auth_entry)
    db.commit()
    db.refresh(db_auth_entry)
    return db_auth_entry

@router.get("/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    # Add logic to read an item by its ID
    pass

@router.put("/{id}/")
def update_item(id: int, item: UserAuthenticationBase, db: Session = Depends(get_db)):
    # Add logic to update an item by its ID
    pass

@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    # Add logic to delete an item by its ID
    pass
