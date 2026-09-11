import bcrypt
from jose import jwt


# Secret key used to create and verify JWT tokens
SECRET_KEY = "my-super-secret-key"

# Algorithm used for JWT token signing
ALGORITHM = "HS256"


# -------------------------------------------------
# Password Hashing
# -------------------------------------------------

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


# -------------------------------------------------
# Password Verification
# -------------------------------------------------

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Check whether the entered password matches
    the password hash stored in the database.
    """

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


# -------------------------------------------------
# JWT Access Token
# -------------------------------------------------

def create_access_token(email: str) -> str:
    """
    Create a JWT access token for an authenticated user.

    The user's email is stored in the 'sub' (subject)
    field of the token.
    """

    payload = {
        "sub": email
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# Decode a JWT token and return the user's email
def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except Exception:
        return None