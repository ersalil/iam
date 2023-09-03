
from pydantic import BaseModel
from typing import Optional

# Base model
class ClientTypeBase(BaseModel):
    clientname: str
    description: Optional[str] = None

# Model for creating a new ClientType
class ClientTypeCreate(ClientTypeBase):
    pass

# Model for updating an existing ClientType
class ClientTypeUpdate(ClientTypeBase):
    pass

# Model for reading the ClientType details
class ClientType(ClientTypeBase):
    ClientTypeID: int

    class Config:
        orm_mode = True
