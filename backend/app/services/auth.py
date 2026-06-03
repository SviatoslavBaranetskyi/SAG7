from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, email: str, username: str, password: str):
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="User already exists")

    user = create_user(
        db=db,
        email=email,
        username=username,
        hashed_password=hash_password(password),
    )

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
    )

    return token