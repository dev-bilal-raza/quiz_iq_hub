from typing import Annotated
from fastapi import Depends, HTTPException

from quizbackend.controllers.admin_controller import (
    add_marks, admin_login_func, admin_verify_func, delete_admin_token_from_db, add_category, add_quiz)
from quizbackend.controllers.openai_controller import generate_question
from quizbackend.models.quiz_model import Category
from quizbackend.routes.userRoute import app
from quizbackend.controllers.auth_controller import passwordIntoHash
from quizbackend.utils.apierrors import NotFoundException
from quizbackend.models.admin_model import Admin, AdminBaseModel
from quizbackend.db.db_connector import DB_SESSION


# ================================================================================================================================
@app.post("/api/adminLogin")
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
@app.get("/api/verifyAdmin")
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
@app.delete("/api/deleteToken")
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
@app.post("/api/adminSign")
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


# ================================================================================================================================
@app.post("/api/addCategory", response_model=list[Category])
def addCategory(categories: Annotated[list[Category], Depends(add_category)]):
    """
    Add category endpoint.

    Args:
        categories (Annotated[list[Category], Depends(add_category)]): List of categories to add.

    Returns:
        list[Category]: List of added categories.

    Raises:
        HTTPException: If categories have not been added.
    """
    # Check if categories exist
    if categories:
        return categories

    # Raise HTTPException if categories have not been added
    raise HTTPException(status_code=404, detail="Category have not been added")


@app.get("/api/generate_mcqs")
async def generateMcqs(category: int, session: DB_SESSION):
    openAi_mcq = generate_question(category=category, session=session)
    if not openAi_mcq:
        raise NotImplementedError("MCQ could not be generated")
    return openAi_mcq


# ================================================================================================================================
@app.post("/api/addQuiz")
def addQuiz(add_question_message: Annotated[str, Depends(add_quiz)]):
    """
    Add quiz endpoint.

    Args:
        add_question_message (Annotated[str, Depends(add_quiz)]): Message indicating the success of adding the quiz.

    Returns:
        str: Message indicating the success of adding the quiz.

    Raises:
        HTTPException: If the quiz could not be added.
    """
    # Check if the add_question_message exists
    if add_question_message:
        return add_question_message

    # Raise HTTPException if the quiz could not be added
    raise HTTPException(status_code=404, detail="Quiz could not be added")


# ================================================================================================================================
@app.post("/api/addMarks")
def addMarks(category_id: int, marks: int, session: DB_SESSION):
    """
    Add marks endpoint.

    Args:
        category_id (int): The ID of the category.
        marks (int): The marks to be added.
        session (DB_SESSION): The database session.

    Returns:
        None
    """
    # Call the add_marks function to add marks
    add_marks(category_id, marks, session)
