
from jose import JWTError, jwt
from fastapi import Depends
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from schemas.user_schemas import UserBase, UserSessionCreate
from sqlalchemy.orm import Session
from database.database import SessionLocal
from routers.usersession_router import create_item
from database.database import get_db

# Placeholder secret key - In production, use a more secure method to store this.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    useremail: Optional[str] = None
    role_id: Optional[UUID] = None
    client_type_id: Optional[UUID] = None
    expires_at: Optional[datetime]

def create_access_token(data: UserBase, expires_delta: timedelta = None, db: Session = Depends(get_db)):    

    token_data = {
        'email': str(data.email),
        'roleid': str(data.roleid),
        'clienttypeid': str(data.clienttypeid)
    }

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    token_data["exp"]= expire
       
    encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    session = {
        "userid": data.userid,
        "sessiontoken": encoded_jwt,
        "expirydate": expire
    }
    if not create_item(item=session, db=db):
        raise Exception("Could not create new session.")

    return {"access_token": encoded_jwt, "access_type": 'bearer'}