from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.models.user_model import Token, User
from app.utils.apierrors import InvalidInputException, NotFoundException
from app.controllers.auth_controller import auth
from app.config.settings import ACCESS_TOKEN_EXPIRE_TIME, REFRESH_TOKEN_EXPIRE_TIME


# define a Bearer token schema on "/token"  url
auth_schema = OAuth2PasswordBearer(tokenUrl="/token")


def logIn_func(user_email: str, user_password: str, session: Session):
    """
    Log in a user.

    Args:
        user_email (str): The email of the user.
        user_password (str): The password of the user.
        session (Session): Database session.

    Raises:
        InvalidInputException: Raised if the email or password is invalid.
        NotFoundException: Raised if the token is not found.

    Returns:
        dict: Access and refresh tokens for the user.
    """
    # Retrieve the user from the database based on the provided email
    user_exist = session.exec(select(User).where(
        User.user_email == user_email)).first()

    # Check if the user exists
    if not user_exist:
        raise InvalidInputException("Email")

    # Verify the provided password against the hashed password stored in the database
    pass_verification_status = auth.verifyPassword(
        user_password, user_exist.user_password)

    # If password verification fails, raise an exception
    if not pass_verification_status:
        raise InvalidInputException("Password")

    # Prepare user data for token generation
    user_data = {
        "user_name": user_exist.user_name,
        "user_email": user_exist.user_email
    }

    # Generate access and refresh tokens
    access_token = auth.generateToken(
        data=user_data, expires_delta=ACCESS_TOKEN_EXPIRE_TIME)
    refresh_token = auth.generateToken(
        data=user_data, expires_delta=REFRESH_TOKEN_EXPIRE_TIME)

    # If tokens are not generated, raise an exception
    if not (access_token or refresh_token):
        raise NotFoundException("Token")
    
    addTokenInDB(user_exist.user_id, refresh_token, session)
    # Return the access and refresh tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def addTokenInDB(user_id: int | None, refresh_token: str, session: Session):
    # Check if a refresh token already exists for the user
    selected_token = session.exec(select(Token).where(
        Token.user_id == user_id)).one_or_none()

    # If no refresh token exists, create a new token entry in the database
    if selected_token is None:
        token = Token(user_id=user_id, refresh_token=refresh_token)
        session.add(token)
        session.commit()
    else:
        # Update the existing refresh token
        selected_token.refresh_token = refresh_token
        session.commit()


def getUserDetails(user: Annotated[User | bool, Depends(auth.verifyUser)]):
    """
    Get user details based on the provided token.

    Args:
        token (str): Authentication token obtained from the client.
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Raises:
        NotFoundException: Raised if the token or user is not found.

    Returns:
        User: User details fetched from the database.
    """
    # If user is not found in the database, raise an exception
    if not user:
        raise NotFoundException("User")

    return user
