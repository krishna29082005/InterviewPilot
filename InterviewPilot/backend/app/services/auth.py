from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.schemas.auth import UserSignup


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
        hashed_password=hash_password(user.password)
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


def login_user(form_data: OAuth2PasswordRequestForm, db: Session):

    existing_user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    if not verify_password(
    form_data.password,
    existing_user.hashed_password
):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }