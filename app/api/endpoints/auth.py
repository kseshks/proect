from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import login

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login_endpoint(login_data: LoginRequest, db: Session = Depends(get_db)):
    return login(db, login_data.identifier, login_data.password)