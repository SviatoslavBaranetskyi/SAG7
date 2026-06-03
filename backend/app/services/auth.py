from sqlalchemy.orm import Session

from app.repositories.user import get_user_by_email, create_user
from app.core.security import hash_password


def register_user(db: Session, email: str, username: str, password: str):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise ValueError("User already exists")

    hashed = hash_password(password)

    user = create_user(
        db=db,
        email=email,
        username=username,
        hashed_password=hashed,
    )

    return user