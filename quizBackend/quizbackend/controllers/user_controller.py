from typing import Annotated
from fastapi import Body, Depends, HTTPException, Response
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from quizbackend.db.db_connector import get_session, DB_SESSION
from quizbackend.models.user_model import UpdateUserModel, User, Token
from quizbackend.utils.apierrors import InvalidInputException, NotFoundException, ConflictsException
from quizbackend.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_TIME, REFRESH_TOKEN_EXPIRE_TIME
import quizbackend.controllers.auth_controller as auth

# define a Bearer token schema on "/token"  url
auth_schema = OAuth2PasswordBearer(tokenUrl="/token")


# =================================================================================================================================
def signup_func(user_name: str, user_email: str, user_password: str, session: Session):
    """
    Register a new user.

    Args:
        user_name (str): The name of the user.
        user_email (str): The email of the user.
        user_password (str): The password of the user.
        session (Session): Database session.

    Raises:
        ConflictsException: Raised if the email or password already exists.

    Returns:
        dict: Data of the logged-in user.
    """
    users = session.exec(select(User))

    for user in users:
        password_exist = auth.verifyPassword(user_password, user.user_password)
        if user.user_email == user_email and password_exist:
            raise ConflictsException("email and password")
        elif user.user_email == user_email:
            raise ConflictsException("email")
        elif password_exist:
            raise ConflictsException("password")

    # Hash the password before storing it
    hash_password = auth.passwordIntoHash(user_password)
    user = User(user_name=user_name,
                user_email=user_email, user_password=hash_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    # Login the newly registered user and return the data
    data = logIn_func(user.user_email, user_password, session)
    print("data from login", data)
    return data


# =================================================================================================================================
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
    access_token = auth.generateAccessToken(
        data=user_data, expires_delta=ACCESS_TOKEN_EXPIRE_TIME)
    refresh_token = auth.generateRefreshToken(
        data=user_data, expires_delta=REFRESH_TOKEN_EXPIRE_TIME)

    # If tokens are not generated, raise an exception
    if not (access_token or refresh_token):
        raise NotFoundException("Token")

    # Check if a refresh token already exists for the user
    selected_token = session.exec(select(Token).where(
        Token.user_id == user_exist.user_id)).first()

    # If no refresh token exists, create a new token entry in the database
    if selected_token is None:
        token = Token(user_id=user_exist.user_id, refresh_token=refresh_token)
        session.add(token)
        session.commit()
    else:
        # Update the existing refresh token
        selected_token.refresh_token = refresh_token
        session.commit()

    # Return the access and refresh tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# =================================================================================================================================
def logout_func(user_id: int, session: DB_SESSION):
    """
    Log out a user by deleting their token from the database.

    Args:
        user_id (int): The ID of the user.
        session (Annotated[Session, Depends(get_session)]): Database session.

    Raises:
        NotFoundException: Raised if the user or token is not found.

    Returns:
        str: Confirmation message indicating successful token deletion.
    """
    # Check if the user ID is provided
    if not user_id:
        raise NotFoundException("User")

    # Retrieve the token associated with the user
    token_table = session.exec(
        select(Token).where(Token.user_id == user_id)).one_or_none()

    # If no token is found, raise an exception
    if not token_table:
        raise NotFoundException("Token")

    # Delete the token from the database
    session.delete(token_table)
    session.commit()

    # Return a confirmation message
    return "Token has been deleted successfully"


# =================================================================================================================================
def deleteUser_func(userId: int, session: Session):
    """
    Delete a user from the database.

    Args:
        userId (int): The ID of the user to be deleted.
        session (Session): Database session.

    Raises:
        NotFoundException: Raised if the user is not found.

    Returns:
        str: Confirmation message indicating successful deletion of the user.
    """
    # Retrieve the user from the database
    user = session.get(User, userId)

    # If user is not found, raise an exception
    if not user:
        raise NotFoundException("User")

    # Delete the user from the database
    session.delete(user)
    session.commit()

    # Return a confirmation message
    return "User has been deleted successfully"


# =================================================================================================================================
def getUserDetails(token: Annotated[str, Depends(auth_schema)], session: Session = Depends(get_session)):
    """
    Get user details based on the provided token.

    Args:
        token (str): Authentication token obtained from the client.
        session (Session, optional): Database session. Defaults to Depends(get_session).

    Raises:
        NotFoundException: Raised if the token or user is not found.
        HTTPException: Raised if the token is invalid.

    Returns:
        User: User details fetched from the database.
    """
    # Check if token is provided
    if not token:
        raise NotFoundException("Token")

    try:
        # Decode the token to extract user information
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    # Extract user email from the decoded token
    user_email = decoded_token["user_email"]

    # If user email is not found, raise an exception
    if not user_email:
        raise NotFoundException("User")

    # Query the database to fetch user details based on the email
    db_user = session.exec(select(User).where(
        User.user_email == user_email)).first()

    # If user is not found in the database, raise an exception
    if not db_user:
        raise NotFoundException("User")

    return db_user


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
        return True
    return False


def updateUserDetails(response: Response, user_Details: UpdateUserModel, verify_user: Annotated[bool, Depends(verifyUser)], session: DB_SESSION):
    print(verify_user)
    # return user_Details
    print(user_Details)
    if not verify_user:
        raise NotFoundException("User")
    user = session.get(User, user_Details.user_id)
    if user:
        user.user_email = user_Details.user_email
        user.user_name = user_Details.user_name
        session.add(user)
        session.commit()
        session.refresh(user)
        # Prepare user data for token generation
        user_data = {
            "user_name": user.user_name,
            "user_email": user.user_email
        }

        # Generate access and refresh tokens
        access_token = auth.generateAccessToken(
            data=user_data, expires_delta=ACCESS_TOKEN_EXPIRE_TIME)
        refresh_token = auth.generateRefreshToken(
            data=user_data, expires_delta=REFRESH_TOKEN_EXPIRE_TIME)

        # If tokens are not generated, raise an exception
        if not (access_token or refresh_token):
            raise NotFoundException("Token")

        # Check if a refresh token already exists for the user
        selected_token = session.exec(select(Token).where(
            Token.user_id == user.user_id)).one_or_none()

        # If no refresh token exists, create a new token entry in the database
        if selected_token:
            # Update the existing refresh token
            selected_token.refresh_token = refresh_token
            session.commit()

        # Calculate expiration time for access and refresh tokens
        access_expire = int(ACCESS_TOKEN_EXPIRE_TIME.total_seconds())
        refresh_expire = int(REFRESH_TOKEN_EXPIRE_TIME.total_seconds())

        # Return the access and refresh tokens
        response.set_cookie("access_token", access_token,
                            expires=access_expire, secure=True)
        response.set_cookie("refresh_token", refresh_token,
                            expires=refresh_expire, secure=True)

        return "User has been updated successfully"
    raise NotFoundException("User")
