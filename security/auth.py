
from passlib.context import CryptContext
from jose import JWTError
from .jwt import create_access_token, TokenData, ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def decode_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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
