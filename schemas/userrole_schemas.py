
from pydantic import BaseModel
from typing import Optional

# Base model
class UserRoleBase(BaseModel):
    clienttypeid: int
    rolename: str
    description: Optional[str] = None

# Model for creating a new UserRole
class UserRoleCreate(UserRoleBase):
    pass

# Model for updating an existing UserRole
class UserRoleUpdate(UserRoleBase):
    pass

# Model for reading the UserRole details
class UserRole(UserRoleBase):
    roleid: int

    class Config:
        orm_mode = True
