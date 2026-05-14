from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.schemas import UserRegister, UserLogin

from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "error": "Email already registered"
        }

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "User Registered"
    }


@router.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Wrong password"}

    token = create_access_token({
        "sub": db_user.email,
        "role": db_user.role
    })

    return {
        "access_token": token
    }