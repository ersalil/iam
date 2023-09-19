
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import UserAuthentication
from schemas.user_schemas import UserAuthenticationBase
from security.auth import hash_password
from datetime import datetime
from database.database import get_db
import cv2, pytesseract
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
import numpy as np
from services.doc_verification import scan_document

router = APIRouter()

@router.post("/")
def create_item(item: UserAuthenticationBase, db: Session = Depends(get_db)):
    try:
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
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

@router.post("/doc/")
async def scan_document(document: UploadFile = Form(...), document_type: str = Form(...)):
    try:
        # Read the image
        image_content = await document.read()
        image_np = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        extracted_data = scan_document(image, document_type)

        return {"document_type": document_type, "extracted_data": extracted_data}

    except Exception as e:
        return HTTPException(detail=str(e), status_code=HTTP_400_BAD_REQUEST)


