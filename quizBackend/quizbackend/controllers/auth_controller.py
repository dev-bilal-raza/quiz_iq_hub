from typing import Annotated
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import select, Session

from quizbackend.controllers.user_controller import auth_schema
from quizbackend.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_TIME
from quizbackend.utils.apierrors import NotFoundException
from quizbackend.db.db_connector import get_session
from quizbackend.models.user_model import Token
from quizbackend.controllers.user_controller import getUserDetails


# Password context for hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===============================================================================================================================
def generateAccessToken(data: dict, expires_delta: timedelta) -> str:
    """
    Generate an access token.

    Args:
        data (dict): User data to be encoded.
        expires_delta (timedelta): Expiry time for the token.

    Returns:
        str: Generated access token.
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
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
    
# ===============================================================================================================================
def generateRefreshToken(data: dict, expires_delta: timedelta) -> str:
    """
    Generate a refresh token.

    Args:
        data (dict): User data to be encoded.
        expires_delta (timedelta): Expiry time for the token.

    Returns:
        str: Generated refresh token.
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
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


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
def tokenService(token: Annotated[str, Depends(auth_schema)], session: Annotated[Session, Depends(get_session)]):
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
    access_token = generateAccessToken(user_data, expires_delta=ACCESS_TOKEN_EXPIRE_TIME)
    
    # Check if the access token was successfully generated
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid Token ")

    return access_token

