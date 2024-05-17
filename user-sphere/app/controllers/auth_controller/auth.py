from typing import Annotated
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import select

from app.config.database import DB_SESSION
from app.models.user_model import User
from app.controllers.auth_controller.auth import auth_schema
from app.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_TIME
from app.utils.apierrors import NotFoundException
from app.models.user_model import Token
from app.controllers.crud_controller.authenticate_user import getUserDetails


# Password context for hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===============================================================================================================================
def generateToken(data: dict, expires_delta: timedelta) -> str:
    """
    Generate a token.

    Args:
        data (dict): User data to be encoded.
        expires_delta (timedelta): Expiry time for the token.

    Returns:
        str: Generated token.
    """
    to_encode = data.copy()
    # Print user data
    print("user", data)
    # Calculate expiry time
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire
    })
    # Encode token with user data and secret key
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ===============================================================================================================================
def passwordIntoHash(password: str) -> str:
    """
    Hashes the provided password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    hash_password = pwd_context.hash(password)
    return hash_password

def verifyUser(token: Annotated[str, Depends(auth_schema)], session: DB_SESSION):
    # Check if token is provided
    if not token:
        raise NotFoundException("Token")
    try:
        # Decode the token to extract user information
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    user_email = decoded_token["user_email"]
    db_user = session.exec(select(User).where(
        User.user_email == user_email)).one_or_none()

    if db_user:
        return db_user
    return False


# ===============================================================================================================================
def verifyPassword(plainText: str, hashedPassword: str) -> bool:
    """
    Verifies if the provided plaintext password matches the hashed password.

    Args:
        plainText (str): The plaintext password.
        hashedPassword (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    # Print the plaintext and hashed passwords for debugging
    print(plainText, hashedPassword)

    # Verify if the plaintext password matches the hashed password
    isPasswordCorrect = pwd_context.verify(plainText, hash=hashedPassword)

    # Print the result of password verification for debugging
    print(isPasswordCorrect)

    return isPasswordCorrect


# ===============================================================================================================================
def tokenService(token: Annotated[str, Depends(auth_schema)], session: DB_SESSION):
    """
    Service function to generate an access token from a refresh token.

    Args:
        token (str): Refresh token.
        session (Session): Database session.

    Returns:
        str: Generated access token.

    Raises:
        NotFoundException: If the token is not found in the database.
        HTTPException: If the access token cannot be generated.
    """
    print(token)
    # Retrieve the refresh token from the database
    db_token = session.exec(select(Token).where(Token.refresh_token == token)).one()
    
    # Check if the token exists
    if not db_token:
        raise NotFoundException("Token")

    # Get user details based on the refresh token
    db_user = getUserDetails(token=db_token.refresh_token, session=session)
    
    # Prepare user data for token generation
    user_data = {
        "user_name": db_user.user_name,
        "user_email": db_user.user_email
    }
    
    # Generate an access token
    access_token = generateToken(user_data, expires_delta=ACCESS_TOKEN_EXPIRE_TIME)
    
    # Check if the access token was successfully generated
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid Token ")

    return access_token

