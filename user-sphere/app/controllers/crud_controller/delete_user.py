from sqlmodel import Session, select
from app.config.database import DB_SESSION
from app.models.user_model import Token, User
from app.utils.apierrors import NotFoundException


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
