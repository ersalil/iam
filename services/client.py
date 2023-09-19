from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.models import ClientType
from schemas.clienttype_schemas import ClientTypeBase, ClientTypeCreate
from database.database import get_db
from uid import unique_id
from routers.userrole_router import create_item as role_init
from routers.clienttype_router import create_item as client_init
from routers.permission_router import create_item as permission_init
from routers.userrolepermission_router import create_item as user_access
from routers.auth_router import signup


router = APIRouter()

def init(item: ClientTypeCreate, db: Session = Depends(get_db)):
    client_data = client_init(item, db)
    data = {
        'clienttypeid': client_data.clienttypeid,
        'rolename': 'Admin',
        'description': 'Initiation'
    }
    role_data = role_init(data, db)
    data = {
        'permissionname': 'Super Admin',
        'description': 'Initiation'
    }
    permission_data = permission_init(data, db)
    user_access({'roleid':role_data.roleid,'permissionid':permission_data.permissionid}, db)
    credentials = {
        "clienttypeid": client_data.clienttypeid,
        "roleid": role_data.roleid,
        "username": client_data.clientname,
        "email": "admin@mal.com",
        "phonenumber": "9999999998",
        "status": "Active",
        "creationdate": "2023-09-18T02:17:15.446Z",
        "lastlogin": "2023-09-18T02:17:15.446Z",
        "password": "Admin@1234"
        }
    signup(credentials, db)
    return client_data
    