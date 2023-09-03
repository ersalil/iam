from fastapi import APIRouter
from pydantic import BaseModel

# Import individual routers from their respective files
from . import user_router, clienttype_router, userrole_router

router = APIRouter()

# Include the individual routers under this parent router
router.include_router(user_router.router, prefix="/user")
router.include_router(clienttype_router.router, prefix="/clienttype")
router.include_router(userrole_router.router, prefix="/userrole")
# router.include_router(authenticationmethod_router)
# router.include_router(userauthentication_router)
# router.include_router(otp_router)
# router.include_router(permission_router)
# router.include_router(userrolepermission_router)
# router.include_router(auditlog_router.router)
# router.include_router(governmentdocument_router)
# router.include_router(usersession_router)

class InfoResponse(BaseModel):
    name: str
    version: str
    status: str
    description: str

@router.get("/info", response_model=InfoResponse)
def get_info():
    return {
        "name": "HorizonHold",
        "version": "1.0.0",
        "status": "green",
        "description": "Holding not only user identity but every thing related to the identification."
    }