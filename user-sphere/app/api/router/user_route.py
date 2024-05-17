from typing import Annotated
from fastapi import APIRouter, Depends, Response

from app.config.database import DB_SESSION
from app.config.settings import ACCESS_TOKEN_EXPIRE_TIME, REFRESH_TOKEN_EXPIRE_TIME
from app.controllers.crud_controller.authenticate_user import logIn_func
from app.controllers.crud_controller.create_user import signup_func
from app.controllers.crud_controller.delete_user import deleteUser_func, logout_func
from app.controllers.crud_controller.update_user import updateUserDetails
from app.models.user_model import UserLogInModel, UserSignUpModel
from app.utils.apierrors import InvalidInputException, NotFoundException

router = APIRouter()

# =================================================================================================================================
@router.post("/api/signup", response_model=str)
async def signup(response: Response, user_signup_form: UserSignUpModel, session: DB_SESSION):
    """
    Endpoint for user signup.

    Args:
        user_signup_form (UserSignUpModel): User signup form data.
        session (DB_SESSION): Database session.

    Raises:
        InvalidInputException: If required fields in the signup form are not provided.

    Returns:
        dict: Dictionary containing access token and refresh token along with their expiration time.
    """
    # Check if required fields in the signup form are provided
    if not (user_signup_form.user_name and user_signup_form.user_email and user_signup_form.user_password):
        raise InvalidInputException("Signup form")

    # Call signup function to perform user signup
    data = signup_func(**user_signup_form.model_dump(), session=session)

    # Calculate expiration time for access and refresh tokens
    access_expire = int(ACCESS_TOKEN_EXPIRE_TIME.total_seconds())
    refresh_expire = int(REFRESH_TOKEN_EXPIRE_TIME.total_seconds())

    response.set_cookie(
        "access_token", data["access_token"], expires=access_expire, secure=True)
    response.set_cookie(
        "refresh_token", data["refresh_token"], expires=refresh_expire, secure=True)

    # Return tokens along with their expiration time
    return "User has been added successfully"


# =================================================================================================================================
@router.post("/api/login", response_model=str)
async def login(response: Response, user_login_form: UserLogInModel, session: DB_SESSION):
    """
    Endpoint for user login.

    Args:
        user_login_form (UserLogInModel): User login form data.
        session (DB_SESSION): Database session.

    Returns:
        dict: Dictionary containing access token and refresh token along with their expiration time.
    """
    # Call the logIn_func function to authenticate the user and obtain tokens
    access_token, refresh_token = logIn_func(
        **user_login_form.model_dump(), session=session).values()

    # Calculate expiration time for access and refresh tokens
    access_expire = int(ACCESS_TOKEN_EXPIRE_TIME.total_seconds())
    refresh_expire = int(REFRESH_TOKEN_EXPIRE_TIME.total_seconds())

    response.set_cookie("access_token", access_token,
                        expires=access_expire, secure=True)
    response.set_cookie("refresh_token", refresh_token,
                        expires=refresh_expire, secure=True)

    # Return tokens along with their expiration time
    return "User has been authenticated successfully"


# =================================================================================================================================
@router.delete("/api/logout", response_model=str)
async def logout(response: Response, delete_token_message: Annotated[str, Depends(logout_func)]):
    """
    Endpoint to logout a user by deleting their token.

    Args:
        delete_token_message (Annotated[str, Depends(logout_func)]): Message indicating successful token deletion.

    Returns:
        str: Message indicating successful token deletion.
    """
    if delete_token_message:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return delete_token_message


# =================================================================================================================================
@router.delete("/api/userDelete")
async def deleteUser(id: int, session: DB_SESSION):
    """
    Endpoint to delete a user.

    Args:
        id (int): User ID to be deleted.
        session (DB_SESSION): Database session.

    Returns:
        str: Message indicating whether the user has been deleted successfully.
    """
    # Call the deleteUser_func function to delete the user
    message = deleteUser_func(id, session)
    # Return the message indicating the status of user deletion
    return message


# =================================================================================================================================
@router.post("/api/update_user", response_model=str)
def updateUser(update_message: Annotated[str, Depends(updateUserDetails)]):
    if update_message:
        return update_message
    raise NotFoundException("User")
