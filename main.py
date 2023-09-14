from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from datetime import datetime
import uuid
import logging
from sqlalchemy.orm import Session

# Imports from the project structure
from database.database import engine, Base
from models.models import User
from security.auth import verify_password, get_password_hash, decode_token
from security.jwt import TokenData, ALGORITHM, SECRET_KEY, create_access_token
from security.otp import generate_otp
from security.email_sender import send_email
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routers import app_v1_router

# Database initialization
Base.metadata.create_all(bind=engine)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Middleware to add a unique ID to each request, useful for logging and debugging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request.state.correlation_id = str(uuid.uuid4())
    logger.info(f"Request ID: {request.state.correlation_id} - URL: {request.url}")
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request ID: {request.state.correlation_id} - Process Time: {process_time}s")
    return response

@app.get('/')
def main_app():
    return "MAIN PAGE"

# Register routers
app.include_router(app_v1_router.router, prefix="/app/v1")