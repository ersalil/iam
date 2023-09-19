from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import ClientType
from schemas.clienttype_schemas import ClientTypeBase, ClientTypeCreate
from database.database import get_db
from uid import unique_id


router = APIRouter()

@router.post("/")
def create_item(item: ClientTypeCreate, db: Session = Depends(get_db)):
    if type(item) != dict:
            item = item.dict()
    item['clienttypeid'] = unique_id()
    db_item = ClientType(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{id}/")
def read_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(ClientType).filter(ClientType.ClientTypeID == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{id}/")
def update_item(id: int, item: ClientTypeBase, db: Session = Depends(get_db)):
    db_item = db.query(ClientType).filter(ClientType.ClientTypeID == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{id}/")
def delete_item(id: str, db: Session = Depends(get_db)):
    db_item = db.query(ClientType).filter(ClientType.clienttypeid == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"status": "Item deleted successfully"}