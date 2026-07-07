from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserSignup

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def signup_user(user: UserSignup, db: Session):

    existing_username = (
        db.query(User)
        .filter(User.username == user.name)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )

    existing_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists."
        )

    new_user = User(
        username=user.name,
        email=user.email,
        hashed_password=pwd_context.hash(user.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()
        raise

    return {
        "message": "User registered successfully."
    }