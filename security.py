import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone


# Secret key used to create and verify JWT tokens
SECRET_KEY = "my-super-secret-key"

# Algorithm used for JWT token signing
ALGORITHM = "HS256"


# -------------------------
# Password Hashing
# -------------------------

def hash_password(password: str) -> str:
    """
    Hash a plain-text password before storing it
    in the database.
    """

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    return hashed_password.decode()


# -------------------------
# Password Verification
# -------------------------

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Check whether the entered password matches
    the password hash stored in the database.
    """

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


# -------------------------
# JWT Access Token
# -------------------------

def create_access_token(email: str) -> str:
    """
    Create a JWT access token for an authenticated user.

    The token expires after 24 hours.
    """

    expire = datetime.now(timezone.utc) + timedelta(hours=24)

    payload = {
        "sub": email,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# -------------------------
# Decode JWT Access Token
# -------------------------

def decode_access_token(token: str) -> str | None:
    """
    Decode the JWT token and return the user's email.

    An expired or invalid token returns None.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except Exception:
        return None