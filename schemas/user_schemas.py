from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base model
class UserBase(BaseModel):
    clienttypeid: int
    roleid: int
    username: str
    email: str
    phonenumber: str
    status: str
    creationdate: datetime
    lastlogin: datetime

# Model for creating a new User
class UserCreate(UserBase):
    clienttypeid: int
    roleid: int
    username: str
    email: str
    phonenumber: str
    status: str
    creationdate: datetime
    lastlogin: datetime

# Model for updating an existing User
class UserUpdate(UserBase):
    pass

# Model for reading the User details
class User(UserBase):
    UserID: int

    class Config:
        orm_mode = True