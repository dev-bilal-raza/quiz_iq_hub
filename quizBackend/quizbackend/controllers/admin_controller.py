from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from typing import Annotated

from quizbackend.controllers.auth_controller import verifyPassword
from quizbackend.controllers.user_controller import auth_schema
from quizbackend.models.admin_model import Admin, AdminBaseModel, AdminToken, QuestionModel, CategoryModel
from quizbackend.models.quiz_model import Category, CategoryMarks, Question, Choice
from quizbackend.settings import ADMIN_TOKEN_EXPIRE_TIME, ALGORITHM, ADMIN_SECRET_KEY
from quizbackend.utils.apierrors import ConflictsException, NotFoundException
from quizbackend.db.db_connector import get_session


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


# ================================================================================================================================
def add_category(user_category: CategoryModel, token: Annotated[str, Depends(admin_verify_func)], session: Annotated[Session, Depends(get_session)]):
    """
    Add a new category.

    Args:
        user_category (CategoryModel): Category information provided by the user.
        token (Annotated[str, Depends(admin_verify_func)]): Admin token.
        session (Annotated[Session, Depends(get_session)]): Database session.

    Returns:
        list[Category]: List of all categories after adding the new one.

    Raises:
        NotFoundException: If the token is not found.
        ConflictsException: If the category already exists.
    """
    # Check if the token exists
    if not token:
        raise NotFoundException("Token")
    # Get all existing categories from the database
    all_categories = session.exec(select(Category)).all()
    # Check if the provided category already exists
    for db_category in all_categories:
        if user_category.category.lower() == db_category.category_name.lower():
            raise ConflictsException("Category")
    # Create a new category instance
    category = Category(category_name=user_category.category,
                        category_description=user_category.category_description)
    # Add the new category to the database
    session.add(category)
    session.commit()
    # Refresh the session to get the newly generated category id
    session.refresh(category)
    # Create a corresponding entry in the CategoryMarks table
    category_marks_table = CategoryMarks(
        category_id=category.category_id, marks=user_category.category_marks)
    session.add(category_marks_table)
    session.commit()
    # Get updated list of all categories
    all_categories = session.exec(select(Category)).all()
    return all_categories


# ================================================================================================================================
def add_marks(category_id: int, marks: int, session: Session):
    """
    Add marks for a specific category.

    Args:
        category_id (int): ID of the category.
        marks (int): Marks to be added.
        session (Session): Database session.

    Returns:
        str
    """
    # Create a new entry in the CategoryMarks table
    category_marks = CategoryMarks(category_id=category_id, marks=marks)
    session.add(category_marks)
    session.commit()
    return "Marks has been added successfully"


# ================================================================================================================================
def add_quiz(token: Annotated[str, Depends(admin_verify_func)], question: QuestionModel, session: Annotated[Session, Depends(get_session)]):
    """
    Add a quiz question to the database.

    Args:
        token (str): Admin token for verification.
        question (QuestionModel): Data model representing the question.
        session (Session): Database session.

    Returns:
        str: Success message if the question is added successfully.
    """
    # Verify admin token
    if not token:
        raise NotFoundException("Token")
    
    # Get the category from the database
    category = session.get(Category, question.category_id)
    if not category:
        raise NotFoundException("Category")
    
    # Create choices for the question
    choice01 = Choice(choice=question.choice1["choice"], choice_status=question.choice1["status"])
    choice02 = Choice(choice=question.choice2["choice"], choice_status=question.choice2["status"])
    choice03 = Choice(choice=question.choice3["choice"], choice_status=question.choice3["status"])
    choice04 = Choice(choice=question.choice4["choice"], choice_status=question.choice4["status"])
    
    # Add the question to the database
    add_question = Question(question=question.question, category_id=category.category_id, choices=[choice01, choice02, choice03, choice04])
    session.add(add_question)
    session.commit()
    session.refresh(add_question)
    
    return "Question added successfully"