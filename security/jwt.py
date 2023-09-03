
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Placeholder secret key - In production, use a more secure method to store this.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData:
    username: Optional[str] = None
    role_id: Optional[int] = None
    client_type_id: Optional[int] = None
    expires_at: Optional[datetime]

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
