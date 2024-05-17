from typing import Annotated
from fastapi import Depends, Response
from sqlmodel import Session

from app.config.database import DB_SESSION
from app.config.settings import ACCESS_TOKEN_EXPIRE_TIME, REFRESH_TOKEN_EXPIRE_TIME
from app.models.user_model import UpdateUserModel, User
from app.utils.apierrors import NotFoundException
from app.controllers.auth_controller import auth
from app.controllers.crud_controller.authenticate_user import addTokenInDB as updateToken


def updateUserDetails(response: Response, user_Details: UpdateUserModel, verify_user: Annotated[bool, Depends(auth.verifyUser)], session: DB_SESSION):
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
        access_token = auth.generateToken(
            data=user_data, expires_delta=ACCESS_TOKEN_EXPIRE_TIME)
        refresh_token = auth.generateToken(
            data=user_data, expires_delta=REFRESH_TOKEN_EXPIRE_TIME)
        message = setTokenInCookie(
            user.user_id, access_token, refresh_token, session, response)

        if message:
            return message
    raise NotFoundException("User")


def setTokenInCookie(user_id: int, access_token: str, refresh_token: str, session: Session, response: Response):
    # If tokens are not generated, raise an exception
    if not (access_token or refresh_token):
        raise NotFoundException("Token")
    updateToken(user_id, refresh_token, session)
    # Calculate expiration time for access and refresh tokens
    access_expire = int(ACCESS_TOKEN_EXPIRE_TIME.total_seconds())
    refresh_expire = int(REFRESH_TOKEN_EXPIRE_TIME.total_seconds())

    # Return the access and refresh tokens
    response.set_cookie("access_token", access_token,
                        expires=access_expire, secure=True)
    response.set_cookie("refresh_token", refresh_token,
                        expires=refresh_expire, secure=True)
    return "User has been updated successfully"
