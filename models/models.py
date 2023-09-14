
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database.database import Base, engine
from datetime import datetime

class ClientType(Base):
    __tablename__ = "clienttype"

    clienttypeid = Column(Integer, primary_key=True, index=True)
    clientname = Column(String, index=True)
    description = Column(String)

    roles = relationship("UserRole", back_populates="clienttype")

class UserRole(Base):
    __tablename__ = "userrole"

    roleid = Column(Integer, primary_key=True, index=True)
    clienttypeid = Column(Integer, ForeignKey('clienttype.clienttypeid'))
    rolename = Column(String, index=True)
    description = Column(String)

    clienttype = relationship("ClientType", back_populates="roles")
    users = relationship("User", back_populates="roles")

class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, index=True)
    clienttypeid = Column(Integer, ForeignKey('clienttype.clienttypeid'))
    roleid = Column(Integer, ForeignKey('userrole.roleid'))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phonenumber = Column(String, unique=True)
    status = Column(String)
    creationdate = Column(DateTime, default=datetime.utcnow)
    lastlogin = Column(DateTime)

    roles = relationship("UserRole", back_populates="users")

class AuthenticationMethod(Base):
    __tablename__ = "authmethod"

    methodid = Column(Integer, primary_key=True, index=True)
    methodtype = Column(String, index=True)
    description = Column(String)

class UserAuthentication(Base):
    __tablename__ = "userauthentication"

    userid = Column(Integer, ForeignKey('users.userid'), primary_key=True)
    methodid = Column(Integer, ForeignKey('authmethod.methodid'), primary_key=True)
    value = Column(String)
    verificationstatus = Column(Boolean)
    lastupdated = Column(DateTime, default=datetime.utcnow)

class OTP(Base):
    __tablename__ = "otp"

    otpid = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    methodid = Column(Integer, ForeignKey('authmethod.methodid'))
    code = Column(String)
    creationtime = Column(DateTime, default=datetime.utcnow)
    expirytime = Column(DateTime)

class Permission(Base):
    __tablename__ = "permission"

    permissionid = Column(Integer, primary_key=True, index=True)
    permissionname = Column(String, index=True)
    description = Column(String)

class UserRolePermission(Base):
    __tablename__ = "userrolepermission"

    roleid = Column(Integer, ForeignKey('userrole.roleid'), primary_key=True)
    permissionid = Column(Integer, ForeignKey('permission.permissionid'), primary_key=True)

class AuditLog(Base):
    __tablename__ = "auditlog"

    logid = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    actiontype = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GovernmentDocument(Base):
    __tablename__ = "govdocument"

    documentid = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    documenttype = Column(String)
    documentnumber = Column(String)
    expirydate = Column(DateTime)
    scannedcopypath = Column(String)
    verificationstatus = Column(Boolean)

class UserSession(Base):
    __tablename__ = "usersession"

    sessionid = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    sessiontoken = Column(String)
    creationdate = Column(DateTime, default=datetime.utcnow)
    expirydate = Column(DateTime)
    