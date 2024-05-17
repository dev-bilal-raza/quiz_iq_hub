from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from typing import Annotated

from app.controllers.admin_auth_controller import verifyPassword
from app.models.admin_model import Admin, AdminBaseModel, AdminToken
from app.config.settings import ADMIN_TOKEN_EXPIRE_TIME, ALGORITHM, ADMIN_SECRET_KEY
from app.utils.apierrors import NotFoundException
from app.config.database import get_session

# define a Bearer token schema on "/token"  url
auth_schema = OAuth2PasswordBearer(tokenUrl="/token")
# ================================================================================================================================
def admin_login_func(adminForm: AdminBaseModel, session: Session):
    """
    Function to authenticate admin and generate token.

    Args:
        adminForm (AdminBaseModel): Admin login details.
        session (Session): SQLModel session.

    Raises:
        NotFoundException: Raised when admin not found in the database.
        HTTPException: Raised for server-side errors.

    Returns:
        dict: Admin token and its details.
    """
    try:
        # Check if admin exists in the database
        admin_exist = session.exec(select(Admin).where(
            Admin.admin_email == adminForm.admin_email)).first()
        if admin_exist:
            # Verify admin password
            password_verified = verifyPassword(
                adminForm.admin_password, admin_exist.admin_password)
        else:
            raise NotFoundException("admin")

        if admin_exist and password_verified:
            # Generate token if admin is authenticated
            data = {"admin_email": admin_exist.admin_email}
            admin_token = generate_admin_token(
                data=data, expires_delta=ADMIN_TOKEN_EXPIRE_TIME)
            if admin_token:
                db_admin_token = add_admin_token_in_db(admin_token, session)
            else:
                raise JWTError("Token has not been generated")

            # Return admin token and its details
            return {
                "admin_token": db_admin_token.admin_token,
                "admin_token_id": db_admin_token.admin_tokenId,
                "expiry_time": ADMIN_TOKEN_EXPIRE_TIME
            }
        raise NotFoundException("admin")
    except NotFoundException as nem:
        raise NotFoundException(nem.message)
    except JWTError as je:
        raise HTTPException(
            status_code=500, detail=je.args)


# ================================================================================================================================
def admin_verify_func(token: Annotated[str, Depends(auth_schema)], session:  Annotated[Session, Depends(get_session)]):
    """
    Function to verify admin token.

    Args:
        token (Annotated[str, Depends(auth_schema)]): Admin token.
        session (Annotated[Session, Depends(get_session)]): SQLModel session.

    Raises:
        NotFoundException: Raised when admin token is not found in the database.

    Returns:
        str: Verification message.
    """
    # Get the first Admin token from database based on condition and then verify admin 
    db_admin_token = session.exec(select(AdminToken).where(
        AdminToken.admin_token == token)).first()
    if db_admin_token:
        return "Admin has verified."
    raise NotFoundException("Token")


# ================================================================================================================================
def generate_admin_token(data: dict, expires_delta: timedelta) -> str:
    """
    Generate an admin token.

    Args:
        data (dict): Admin data to be encoded.
        expires_delta (timedelta): Expiry time for the token.

    Returns:
        str: Generated admin token.
    """
    # Make a copy of the admin data
    to_encode = data.copy()
    print("admin", data)
    
    # Calculate the expiry time
    expire = datetime.now(timezone.utc) + expires_delta
    
    # Update the data with the expiry time
    to_encode.update({"exp": expire})
    
    # Encode the data to generate the token
    access_token = jwt.encode(to_encode, ADMIN_SECRET_KEY, algorithm=ALGORITHM)
    return access_token


# ================================================================================================================================
def add_admin_token_in_db(token: str, session: Session):
    """
    Add an admin token to the database.

    Args:
        token (str): Admin token to be added.
        session (Session): Database session.

    Returns:
        AdminToken: Added admin token.
    """
    admin_token = AdminToken(admin_token=token)
    session.add(admin_token)
    session.commit()
    session.refresh(admin_token)
    return admin_token


# ================================================================================================================================
def delete_admin_token_from_db(token_id: int, session: Session):
    """
    Delete an admin token from the database.

    Args:
        token_id (int): ID of the token to be deleted.
        session (Session): Database session.

    Returns:
        str: Confirmation message.
    
    Raises:
        NotFoundException: If the token with the given ID is not found.
    """
    # Get Admin token from database based on token id
    db_admin_token = session.get(AdminToken, token_id)
    if db_admin_token is None:
        raise NotFoundException("Token")
    # Delete the Admin token from database  
    session.delete(db_admin_token)
    session.commit()
    return "Token has been deleted"
