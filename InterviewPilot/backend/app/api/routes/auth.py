from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.auth import signup_user, login_user
from app.api.dependencies.auth import get_current_user
from app.db.database import get_db

from app.schemas.auth import (
    UserSignup,
    Token,
    UserResponse,
    MessageResponse,
)

from app.services.auth import (
    signup_user,
    login_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=MessageResponse,
)
def signup(
    user: UserSignup,
    db: Session = Depends(get_db),
):
    return signup_user(user, db)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_user(form_data, db)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    return current_user