import sqlalchemy

metadata = sqlalchemy.MetaData()
from datetime import datetime

clienttypes = sqlalchemy.Table(
    "clienttypes",
    metadata,
    sqlalchemy.Column("ClientTypeID", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("ClientName", sqlalchemy.String),
    sqlalchemy.Column("Description", sqlalchemy.String, nullable=True)
)

userroles = sqlalchemy.Table(
    "userroles",
    metadata,
    sqlalchemy.Column("RoleID", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("ClientTypeID", sqlalchemy.Integer, sqlalchemy.ForeignKey('clienttypes.ClientTypeID')),
    sqlalchemy.Column("RoleName", sqlalchemy.String),
    sqlalchemy.Column("Description", sqlalchemy.String, nullable=True)
)

auditlogs = sqlalchemy.Table(
    "auditlogs",
    metadata,
    sqlalchemy.Column("LogID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("userid", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.userid')),
    sqlalchemy.Column("ActionType", sqlalchemy.String),
    sqlalchemy.Column("Timestamp", sqlalchemy.DateTime, default=datetime.utcnow)
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("userid", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("ClientTypeID", sqlalchemy.Integer, sqlalchemy.ForeignKey('clienttypes.ClientTypeID')),
    sqlalchemy.Column("RoleID", sqlalchemy.Integer, sqlalchemy.ForeignKey('userroles.RoleID')),
    sqlalchemy.Column("Username", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("Email", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("PhoneNumber", sqlalchemy.String, unique=True),
    sqlalchemy.Column("Status", sqlalchemy.String),
    sqlalchemy.Column("CreationDate", sqlalchemy.DateTime, default=datetime.utcnow),
    sqlalchemy.Column("LastLogin", sqlalchemy.DateTime)
)