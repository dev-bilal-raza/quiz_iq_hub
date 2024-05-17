from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter

from app.controllers.admin_crud_controller import (
    admin_login_func, admin_verify_func, delete_admin_token_from_db)
from app.controllers.admin_auth_controller import passwordIntoHash
from app.utils.apierrors import NotFoundException
from app.models.admin_model import Admin, AdminBaseModel
from app.config.database import DB_SESSION


route = APIRouter()

# ================================================================================================================================
@route.post("/api/adminLogin")
def adminLogin(adminForm: AdminBaseModel, session: DB_SESSION):
    """
    Endpoint for admin login.

    Args:
        adminForm (AdminBaseModel): Admin login form data.
        session (DB_SESSION): Database session.

    Returns:
        dict: Admin token and related details if login successful.

    Raises:
        HTTPException: If admin is not found.
    """
    # Call the admin_login_func to verify admin login
    admin_data = admin_login_func(adminForm, session=session)

    # Return admin data if found
    if admin_data:
        return admin_data

    # Raise HTTPException if admin is not found
    raise HTTPException(status_code=404, detail="Admin not found")


# ================================================================================================================================
@route.get("/api/verifyAdmin")
def adminVerify(verification_message: Annotated[str, Depends(admin_verify_func)]):
    """
    Endpoint for verifying admin.

    Args:
        verification_message (str): Verification message.

    Returns:
        str: Verification message.

    Raises:
        NotFoundException: If token is not found.
    """
    # Check if verification message exists
    if verification_message:
        return verification_message

    # Raise NotFoundException if token is not found
    raise NotFoundException("Token")


# ================================================================================================================================
@route.delete("/api/deleteToken")
def deleteAdminToken(token_id: int, session: DB_SESSION):
    """
    Delete admin token endpoint.

    Args:
        token_id (int): ID of the token to be deleted.
        session (DB_SESSION): Database session.

    Returns:
        str: Delete message.

    Raises:
        NotFoundException: If token is not found.
    """
    # Attempt to delete the token
    delete_message = delete_admin_token_from_db(token_id, session)

    # Check if delete message exists
    if delete_message:
        return delete_message

    # Raise NotFoundException if token is not found
    raise NotFoundException("Token")


# ================================================================================================================================
@route.post("/api/adminSign")
def adminSign(adminForm: AdminBaseModel, session: DB_SESSION):
    """
    Admin signup endpoint.

    Args:
        adminForm (AdminBaseModel): Admin signup form data.
        session (DB_SESSION): Database session.

    Returns:
        Admin: Created admin data.

    Raises:
        HTTPException: If admin data is not found.
    """
    # Hash the admin password
    hashed_password = passwordIntoHash(adminForm.admin_password)

    # Create admin data
    admin_data = Admin(admin_email=adminForm.admin_email,
                       admin_password=hashed_password)

    # Add admin data to the database
    session.add(admin_data)
    session.commit()
    session.refresh(admin_data)

    # Check if admin data exists
    if admin_data:
        return admin_data

    # Raise HTTPException if admin data is not found
    raise HTTPException(status_code=404, detail="Admin not found")
