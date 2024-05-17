from sqlmodel import Session, select

from app.models.user_model import User
from app.utils.apierrors import ConflictsException
from app.controllers.auth_controller import auth
from app.controllers.crud_controller.authenticate_user import logIn_func

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
