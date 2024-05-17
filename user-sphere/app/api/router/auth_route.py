from typing import Annotated
from fastapi import APIRouter, Depends

from app.config.settings import ACCESS_TOKEN_EXPIRE_TIME
from app.controllers.auth_controller.auth import tokenService
from app.controllers.crud_controller.authenticate_user import getUserDetails
from app.models.user_model import User
from app.utils.apierrors import NotFoundException

router = APIRouter()

# =================================================================================================================================
@router.get("/api/getUser", response_model=User)
async def getUser(userData: Annotated[User, Depends(getUserDetails)]):
    """
    Endpoint to retrieve user data.

    Args:
        userData (Annotated[User, Depends(getUserDetails)]): User data obtained from the database.

    Raises:
        NotFoundException: If user data is not found.

    Returns:
        dict: User data with the password removed.
    """
    # Check if user data exists
    if not userData:
        # Raise exception if user data is not found
        raise NotFoundException("User")
    # Extract user data and remove password field
    user = userData.model_dump()
    user.pop("user_password")
    # Return user data
    return user


# =================================================================================================================================
@router.get("/api/getToken", response_model=dict[str, str | int])
async def getToken(accessToken: Annotated[str, Depends(tokenService)]):
    """
    Endpoint to retrieve an access token.

    Args:
        accessToken (Annotated[str, Depends(tokenService)]): Access token obtained from the token service.

    Raises:
        NotFoundException: If the access token is not found.

    Returns:
        dict: Dictionary containing the access token and its expiration time.
    """
    # Check if access token exists
    if not accessToken:
        # Raise exception if access token is not found
        raise NotFoundException("Token")
    # Calculate expiration time of the access token
    access_expire = int(ACCESS_TOKEN_EXPIRE_TIME.total_seconds())
    # Return access token and its expiration time
    return {
        "access_token": accessToken,
        "expires_in": access_expire
    }
