from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import (
    UserRegister,
    UserResponse,
    UserLogin,
    TokenResponse,
)

from app.services.auth import register_user, login_user
from app.db.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(
        db=db,
        email=payload.email,
        username=payload.username,
        password=payload.password,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    token = login_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }