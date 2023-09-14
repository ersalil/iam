
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import GovernmentDocument
from schemas.user_schemas import GovernmentDocumentBase, GovernmentDocumentCreate
from pydantic import BaseModel
import pytesseract
from PIL import Image
import io

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    def perform_ocr(image_content):
     image = Image.open(io.BytesIO(image_content))
     text = pytesseract.image_to_string(image)
     return text

@router.post("/", response_model=GovernmentDocument)
def create_document(item: GovernmentDocumentCreate, db: Session = Depends(get_db), file: UploadFile = File(...)):
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only images are supported.")

    image_content = file.file.read()

    ocr_text = perform_ocr(image_content)

    db_document = GovernmentDocument(**item.dict(), OCRvalue=ocr_text)

    try:
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{documentid}", response_model=GovernmentDocument)
def read_document(documentid: int, db: Session = Depends(get_db)):
    db_document = db.query(GovernmentDocument).filter(GovernmentDocument.documentid == documentid).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.put("/{id}/")
def update_item(id: int, item: GovernmentDocumentBase, db: Session = Depends(get_db)):
    db_document = db.query(GovernmentDocument).filter(GovernmentDocument.documentid == id).first()

    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    for key, value in item.dict().items():
        setattr(db_document, key, value)

    try:
        db.commit()
        db.refresh(db_document)
        return db_document
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    db_document = db.query(GovernmentDocument).filter(GovernmentDocument.documentid == id).first()

    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        db.delete(db_document)
        db.commit()
        return {"detail": "Document deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
