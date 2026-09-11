from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import UserRow, get_db
from security import (
    verify_password,
    create_access_token,
    decode_access_token
)


# -------------------------
# Auth Router
# -------------------------
router = APIRouter(
    tags=["auth"]
)


# -------------------------
# OAuth2 Configuration
# -------------------------
# FastAPI protected routes se Bearer token receive karega.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# -------------------------
# User Login
# -------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2 form mein field ka naam "username" hota hai.
    # Hum is field mein user ka email receive kar rahe hain.
    user = (
        db.query(UserRow)
        .filter(UserRow.email == form_data.username)
        .first()
    )

    # User nahi mila.
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Entered password ko database ke hashed password
    # ke against verify karo.
    password_correct = verify_password(
        form_data.password,
        user.password_hash
    )

    # Password incorrect hai.
    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Login successful hone ke baad JWT token create karo.
    token = create_access_token(user.email)

    # Client ko token return karo.
    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------
# Get Current User
# -------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # JWT se user ka email nikaalo.
    email = decode_access_token(token)

    # Token invalid hai ya email nahi mila.
    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # Email ki help se database mein user find karo.
    user = (
        db.query(UserRow)
        .filter(UserRow.email == email)
        .first()
    )

    # Token valid ho sakta hai lekin user database mein nahi hai.
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Authenticated user return karo.
    return user