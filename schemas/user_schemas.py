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

class SignUp(UserBase):
    clienttypeid: int
    roleid: int
    username: str
    email: str
    phonenumber: str
    status: str
    creationdate: datetime
    lastlogin: datetime
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
    roleid: int
    permissionid: int

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
    userid: int
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
    pass

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
    methodid: int
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
    userid: int
    actiontype: str
    timestamp: datetime

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    logid: int

    class Config:
        orm_mode = True

#Model for UserAuthentication        
class UserAuthenticationBase(BaseModel):
    userid: int
    methodid: int
    value: str
    verificationstatus: bool
    lastupdated: str

class UserAuthenticationCreate(UserAuthenticationBase):
    pass

class UserAuthentication(UserAuthenticationBase):
    class Config:
        orm_mode = True

