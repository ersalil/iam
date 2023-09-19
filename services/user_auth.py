from schemas.user_schemas import AuthSignup, UserBase, AuditLogCreate, UserAuthenticationBase
from security.auth import hash_password
from datetime import datetime
from sqlalchemy.orm import Session
from routers.userauthentication_router import create_item as save_pass
from routers.auditlog_router import create_item as create_audit
from datetime import datetime
from uid import unique_id

def save_password(user: UserBase, password: str, db: Session) -> None:    
    data = {
        'userid':user['userid'],
        'methodid':'9d1886ed-8eb7-4cba-8c5d-60c9d7149104',
        'value':hash_password(password),
        'verificationstatus':True,
        'lastupdated':datetime.now()
    }    
    return save_pass(data, db)
    
        
def create_audit_log(user: UserBase, action_type: str, db: Session) -> None:
    data = {
        'logid': unique_id(),
        'userid':user['userid'],
        'actiontype':action_type,
        'timestamp':datetime.now()
    }
    return create_audit(data, db)
    
    