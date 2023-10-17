
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


# Base model
class UserRoleBase(BaseModel):
    clienttypeid: UUID
    rolename: str
    description: Optional[str] = None

# Model for creating a new UserRole
class UserRoleCreate(UserRoleBase):
    permission_id: Optional[list] = None

# Model for updating an existing UserRole
class UserRoleUpdate(UserRoleBase):
    roleid: UUID

# Model for reading the UserRole details
class UserRole(UserRoleBase):
    roleid: UUID

    class Config:
        orm_mode = True
