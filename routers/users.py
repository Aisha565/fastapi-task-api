from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import UserRow, get_db
from schemas import UserCreate
from security import hash_password


# -------------------------
# Users Router
# -------------------------
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# -------------------------
# Register User
# -------------------------
@router.post("", status_code=201)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if a user with this email already exists.
    existing_user = (
        db.query(UserRow)
        .filter(UserRow.email == user_data.email)
        .first()
    )

    # Prevent duplicate email registration.
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash the password before storing it in the database.
    hashed_password = hash_password(user_data.password)

    # Create a new user database object.
    new_user = UserRow(
        email=user_data.email,
        password_hash=hashed_password
    )

    # Add the new user to the database.
    db.add(new_user)

    # Save the new user permanently.
    db.commit()

    # Refresh the object to get the generated user ID.
    db.refresh(new_user)

    # Return basic user information.
    # Password is never returned.
    return {
        "id": new_user.id,
        "email": new_user.email
    }