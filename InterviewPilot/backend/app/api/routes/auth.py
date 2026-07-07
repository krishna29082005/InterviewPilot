from fastapi import APIRouter
from app.services.auth import signup_user
from app.schemas.auth import UserSignup
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    return signup_user(user, db)