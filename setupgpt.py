# Directory setup for the restructuring
import os
base_dir = '.'

from fastapi import APIRouter

# Directory setup for routers
routers_dir = os.path.join(base_dir, "routers")
os.makedirs(routers_dir, exist_ok=True)

# Utility to save a basic CRUD router for an entity
def save_basic_crud_router(entity_name, primary_key_name, routers_dir):
    router_code = f"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.models import {entity_name}
from ..schemas.schemas import {entity_name}Base, {entity_name}Create

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{entity_name.lower()}/")
def create_item(item: {entity_name}Create, db: Session = Depends(get_db)):
    # Add logic to create an item
    pass

@router.get("/{entity_name.lower()}/{{id}}/")
def read_item(id: int, db: Session = Depends(get_db)):
    # Add logic to read an item by its ID
    pass

@router.put("/{entity_name.lower()}/{{id}}/")
def update_item(id: int, item: {entity_name}Base, db: Session = Depends(get_db)):
    # Add logic to update an item by its ID
    pass

@router.delete("/{entity_name.lower()}/{{id}}/")
def delete_item(id: int, db: Session = Depends(get_db)):
    # Add logic to delete an item by its ID
    pass
"""
    router_path = os.path.join(routers_dir, f"{entity_name.lower()}_router.py")
    with open(router_path, 'w') as file:
        file.write(router_code)
    return router_path

# Creating basic CRUD routers for the entities
router_files = {}
entities = {
    "ClientType": "ClientTypeID",
    "UserRole": "RoleID",
    "User": "UserID",
    "AuthenticationMethod": "MethodID",
    "UserAuthentication": "UserID",
    "OTP": "OTPID",
    "Permission": "PermissionID",
    "UserRolePermission": "RoleID",
    "AuditLog": "LogID",
    "GovernmentDocument": "DocumentID",
    "UserSession": "SessionID"
}

for entity, primary_key in entities.items():
    router_files[entity] = save_basic_crud_router(entity, primary_key, routers_dir)

router_files

router_imports = "\n".join([f"from routers import {entity.lower()}_router" for entity in entities.keys()])
router_includes = "\n".join([f'app.include_router({entity.lower()}_router.router)' for entity in entities.keys()])

print(router_imports)
print('.../n ', router_includes)