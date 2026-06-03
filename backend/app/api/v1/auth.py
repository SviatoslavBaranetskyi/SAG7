from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import UserRegister, UserResponse
from app.services.auth import register_user
from app.db.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    try:
        user = register_user(
            db=db,
            email=payload.email,
            username=payload.username,
            password=payload.password,
        )
        return user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))