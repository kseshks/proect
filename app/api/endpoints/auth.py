from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import log_in

router = APIRouter(prefix="/auth", tags=["Аутентификация"])
@router.post("/login", response_model=Token)
def login_endpoint(login_data: LoginRequest, db: Session = Depends(get_db)):
    return log_in(db, login_data.username, login_data.password)
