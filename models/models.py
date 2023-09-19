
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship
from database.database import Base, engine
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from uuid import uuid4

class ClientType(Base):
    __tablename__ = "clienttype"

    clienttypeid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)

    clientname = Column(String, index=True)
    description = Column(String)

    roles = relationship("UserRole", back_populates="clienttype")

class UserRole(Base):
    __tablename__ = "userrole"

    roleid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    clienttypeid = Column(pgUUID, ForeignKey('clienttype.clienttypeid'))
    rolename = Column(String, index=True)
    description = Column(String)

    clienttype = relationship("ClientType", back_populates="roles")
    users = relationship("User", back_populates="roles")

class User(Base):
    __tablename__ = "users"

    userid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    clienttypeid = Column(pgUUID, ForeignKey('clienttype.clienttypeid'))
    roleid = Column(pgUUID, ForeignKey('userrole.roleid'))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phonenumber = Column(String, unique=True)
    status = Column(String)
    creationdate = Column(DateTime, default=datetime.utcnow)
    lastlogin = Column(DateTime)

    roles = relationship("UserRole", back_populates="users")

class AuthenticationMethod(Base):
    __tablename__ = "authmethod"

    methodid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    methodtype = Column(String, index=True)
    description = Column(String)

class UserAuthentication(Base):
    __tablename__ = "userauthentication"

    userid = Column(pgUUID, ForeignKey('users.userid'), primary_key=True)
    methodid = Column(pgUUID, ForeignKey('authmethod.methodid'), primary_key=True)
    value = Column(String)
    verificationstatus = Column(Boolean)
    lastupdated = Column(DateTime, default=datetime.utcnow)

class OTP(Base):
    __tablename__ = "otp"

    otpid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    userid = Column(pgUUID, ForeignKey('users.userid'))
    methodid = Column(pgUUID, ForeignKey('authmethod.methodid'))
    code = Column(String)
    creationtime = Column(DateTime, default=datetime.utcnow)
    expirytime = Column(DateTime)

class Permission(Base):
    __tablename__ = "permission"

    permissionid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    permissionname = Column(String, index=True)
    description = Column(String)

class UserRolePermission(Base):
    __tablename__ = "userrolepermission"

    roleid = Column(pgUUID, ForeignKey('userrole.roleid'), primary_key=True)
    permissionid = Column(pgUUID, ForeignKey('permission.permissionid'), primary_key=True)

class AuditLog(Base):
    __tablename__ = "auditlog"

    logid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    userid = Column(pgUUID, ForeignKey('users.userid'))
    actiontype = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GovernmentDocument(Base):
    __tablename__ = "govdocument"

    documentid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    userid = Column(pgUUID, ForeignKey('users.userid'))
    documenttype = Column(String)
    documentnumber = Column(String)
    expirydate = Column(DateTime)
    scannedcopypath = Column(String)
    verificationstatus = Column(Boolean)

class UserSession(Base):
    __tablename__ = "usersession"

    sessionid = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    userid = Column(pgUUID, ForeignKey('users.userid'))
    sessiontoken = Column(String)
    creationdate = Column(DateTime, default=datetime.utcnow)
    expirydate = Column(DateTime)
    