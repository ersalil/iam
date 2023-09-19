from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# Base model
class UserBase(BaseModel):
    userid: UUID
    clienttypeid: UUID
    roleid: UUID
    username: str
    email: str
    phonenumber: str
    status: str
    creationdate: datetime
    lastlogin: datetime
    
class UserToken(UserBase):
    userid: UUID

# Model for creating a new User
class UserCreate(BaseModel):
    clienttypeid: UUID
    roleid: UUID
    username: str
    email: str
    phonenumber: str
    status: str
    creationdate: datetime
    lastlogin: datetime
    password: str

class SignUp(UserBase):
    password: str

# Model for updating an existing User
class UserUpdate(UserBase):
    pass

# Model for reading the User details
class User(UserBase):
    userid: int

    class Config:
        orm_mode = True
        
# Model for Userrolepermission
class UserRolePermissionBase(BaseModel):
    roleid: UUID
    permissionid: UUID

class UserRolePermissionCreate(UserRolePermissionBase):
    pass

class UserRolePermissionUpdate(UserRolePermissionBase):
    pass

class UserRolePermission(UserRolePermissionBase):
    id: int

    class Config:
        orm_mode = True
        
#Model for Usersession
class UserSessionBase(BaseModel):
    userid: UUID
    sessiontoken: str  # We can specify the data type for the token field based on your requirements
    expirydate: datetime

class UserSessionCreate(UserSessionBase):
    pass

class UserSessionUpdate(UserSessionBase):
    pass

class UserSession(UserSessionBase):
    sessionid: int
    class Config:
        orm_mode = True
        
# Model for Permission 
class PermissionBase(BaseModel):
    permissionname: str
    description: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    permissionid: UUID

class Permission(PermissionBase):
    Permissionid: int

    class Config:
        orm_mode = True
        
#Model for login
class LoginBase(BaseModel):
    username :str
    password :str

#Model for login
class AuthenticationMethodBase(BaseModel):
    methodtype : str
    description: str
  
#Model for Governmentdocument    
class GovernmentDocumentBase(BaseModel):
    title: str
    description: str
    document_type: str

class GovernmentDocumentCreate(GovernmentDocumentBase):
    pass

class GovernmentDocument(GovernmentDocumentBase):
    id: int

    class Config:
        orm_mode = True
    
#Model for Auditlog
from pydantic import BaseModel
from datetime import datetime

class AuditLogBase(BaseModel):
    logid: UUID
    userid: UUID
    actiontype: str
    timestamp: datetime

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    logid: UUID

    class Config:
        orm_mode = True

#Model for UserAuthentication        
class UserAuthenticationBase(BaseModel):
    userid: UUID
    methodid: UUID
    value: str
    verificationstatus: bool
    lastupdated: datetime

class AuthSignup(UserAuthenticationBase):
    pass

class UserAuthenticationCreate(UserAuthenticationBase):
    pass

class UserAuthentication(UserAuthenticationBase):
    class Config:
        orm_mode = True

