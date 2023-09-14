from passlib.context import CryptContext
from jose import JWTError, jwt
from .jwt import create_access_token, TokenData, ALGORITHM, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from models.models import User
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends
from database.database import SessionLocal
from datetime import datetime
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(plain_password):
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == payload.username).first()
    if user is None:
        raise credentials_exception
    return user
    

def get_password_hash(password):
    return pwd_context.hash(password)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role_id: int = payload.get("role_id")
        client_type_id: int = payload.get("client_type_id")
        expires_at: datetime = payload.get("exp")
        if username is None or role_id is None or client_type_id is None:
            raise credentials_exception
        token_data = TokenData(username=username, role_id=role_id, client_type_id=client_type_id, expires_at=expires_at)
    except JWTError:
        raise credentials_exception
    return token_data
