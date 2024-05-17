from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Any
from contextlib import asynccontextmanager


from quizbackend.db.db_connector import DB_SESSION, create_table
from quizbackend.controllers.quiz_controller import (
    get_categories, get_quiz, attempt_quiz, isAvailableQuiz, getQuizDetails, delete_quiz, get_categories_details)
from quizbackend.controllers.auth_controller import tokenService
from quizbackend.models.quiz_model import Category
from quizbackend.settings import ACCESS_TOKEN_EXPIRE_TIME, REFRESH_TOKEN_EXPIRE_TIME
from quizbackend.models.pydantic_model import QuizAttemptModel
from quizbackend.models.user_model import User, UserSignUpModel, UserLogInModel
from quizbackend.controllers.user_controller import (
    signup_func, logIn_func, deleteUser_func, getUserDetails, logout_func, updateUserDetails)
from quizbackend.utils.apierrors import InvalidInputException, NotFoundException, ConflictsException


# =================================================================================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager to perform setup and teardown operations during the lifespan of the application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Yields control back to the caller.
    """
    # Create necessary database tables
    create_table()
    yield

# Create the FastAPI application instance with the lifespan context manager
app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow cross-origin requests from specified origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)


# Exception handlers for custom exceptions

# =================================================================================================================================
@app.exception_handler(NotFoundException)
async def notFoundException(request: Request, exception: NotFoundException):
    """
    Exception handler for NotFoundException.

    Args:
        request (Request): The incoming request object.
        exception (NotFoundException): The NotFoundException instance.

    Returns:
        JSONResponse: JSON response indicating the error message.
    """
    return JSONResponse(status_code=400, content={"message": f"OMG! {exception.message} not found"})


# =================================================================================================================================
@app.exception_handler(InvalidInputException)
async def invalidInputException(request: Request, exception: InvalidInputException):
    """
    Exception handler for InvalidInputException.

    Args:
        request (Request): The incoming request object.
        exception (InvalidInputException): The InvalidInputException instance.

    Returns:
        JSONResponse: JSON response indicating the error message.
    """
    return JSONResponse(status_code=400, content={"message": f"OOPS! You have not entered correct {exception.message}"})


# =================================================================================================================================
@app.exception_handler(ConflictsException)
async def existingInputException(request: Request, exception: ConflictsException):
    """
    Exception handler for ConflictsException.

    Args:
        request (Request): The incoming request object.
        exception (ConflictsException): The ConflictsException instance.

    Returns:
        JSONResponse: JSON response indicating the error message.
    """
    return JSONResponse(status_code=400, content={"message": f"This {exception.message} already exists. Please choose another."})


# =================================================================================================================================
@app.get("/")
async def main():
    return "Welcome to the Quiz Web!"


# =================================================================================================================================
@app.post("/api/signup")
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
    
    response.set_cookie("access_token", data["access_token"], expires=access_expire, secure=True)
    response.set_cookie("refresh_token", data["refresh_token"], expires=refresh_expire, secure=True)
    
    # Return tokens along with their expiration time
    return "User has been added successfully"


# =================================================================================================================================
@app.post("/api/login")
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
    
    response.set_cookie("access_token", access_token, expires=access_expire, secure=True)
    response.set_cookie("refresh_token", refresh_token, expires=refresh_expire, secure=True)
    
    # Return tokens along with their expiration time
    return "User has been authenticated successfully"


# =================================================================================================================================
@app.delete("/api/logout")
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
@app.get("/api/getUser")
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
@app.get("/api/getToken", response_model=dict[str, str | int])
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


# =================================================================================================================================
@app.delete("/api/userDelete")
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
@app.post("/api/update_user")
def updateUser(update_message: Annotated[str, Depends(updateUserDetails)]):
    if update_message:
        return update_message
    raise NotFoundException("User")


# =================================================================================================================================
@app.get("/api/getQuizCategories", response_model=list[Category])
async def getCategories(session: DB_SESSION):
    """
    Endpoint to get all quiz categories.

    Args:
        session (DB_SESSION): Database session.

    Returns:
        list[Category]: List of quiz categories.
    """
    # Retrieve all quiz categories from the database
    all_categories = get_categories(session)

    # Check if categories are retrieved successfully
    if all_categories:
        return all_categories
    else:
        # If categories retrieval fails, raise an HTTPException
        raise HTTPException(
            status_code=500, detail="Could not get categories. Please try again."
        )


# =================================================================================================================================
@app.get("/api/getQuiz", response_model=dict[str, Any])
async def getQuiz(user_id: int, category_name: str, session: DB_SESSION):
    print(user_id)
    """
    Endpoint to get a quiz for a specific user and category.

    Args:
        user_id (int): User ID.
        category_name (str): Name of the quiz category.
        session (DB_SESSION): Database session.

    Returns:
        dict[str, Any]: Dictionary containing quiz details.
    """
    # Retrieve quiz questions for the specified user and category
    questions = get_quiz(user_id, category_name, session)
    return questions


# =================================================================================================================================
@app.get("/api/isAvailableQuiz", response_model=bool)
async def availableQuiz(category_name: str, session: DB_SESSION):
    """
    Endpoint to check if a quiz is available for a specific category.

    Args:
        category_name (str): Name of the quiz category.
        session (DB_SESSION): Database session.

    Returns:
        bool: True if quiz is available, False otherwise.
    """
    if not category_name:
        # raise not implemented error if category name does not exist
        raise NotImplementedError("Category name")
    return isAvailableQuiz(category_name=category_name, session=session)


# =================================================================================================================================
@app.get("/api/getCategoryQuizDetails")
async def getCategoryQuizDetails(user_id: int, category_name: str, session: DB_SESSION):
    """
    Endpoint to get quiz details for a specific category and user.

    Args:
        user_id (int): User ID.
        category_name (str): Name of the quiz category.
        session (DB_SESSION): Database session.

    Returns:
        dict: Quiz details including remaining questions, marks, and attempt status.
    """
    # Call the getQuizDetails function to retrieve quiz details
    details = getQuizDetails(user_id=user_id,
                             category_name=category_name, session=session)
    return details


# =================================================================================================================================
@app.get("/api/getAllCategoryDetails")
async def getCategoriesDetails(user_id: int, session: DB_SESSION):
    """
    Endpoint to retrieve details of all quiz categories for a specific user.

    Args:
        user_id (int): User ID.
        session (DB_SESSION): Database session.

    Returns:
        dict: Details of all quiz categories including attempt status and total marks.
    """
    # Retrieve details of all quiz categories for the specified user
    categories_details = get_categories_details(user_id, session)
    return categories_details


# =================================================================================================================================
@app.post("/api/attemptQuiz")
async def attemptQuiz(attempt_quiz_form: QuizAttemptModel, session: DB_SESSION):
    """
    Endpoint to attempt a quiz.

    Args:
        attempt_quiz_form (QuizAttemptModel): Data model containing information about the attempted quiz.
        session (DB_SESSION): Database session.

    Returns:
        str: Message indicating the success or failure of the quiz attempt.
    """
    # Print the attempted quiz data
    print(attempt_quiz_form)

    # Attempt the quiz using the provided data and database session
    response_message = attempt_quiz(
        session=session, **attempt_quiz_form.model_dump())

    # Raise exception if no response message is returned
    if not response_message:
        raise NotFoundException("User")

    # Return the response message
    return response_message


# =================================================================================================================================
@app.delete("/api/deleteQuiz")
def deleteQuiz(user_id: int, category_id: int, session: DB_SESSION):
    """
    Endpoint to delete a quiz for a user.

    Args:
        user_id (int): The ID of the user whose quiz is to be deleted.
        category_id (int): The ID of the category for which the quiz is to be deleted.
        session (DB_SESSION): Database session.

    Returns:
        str: Message indicating the success or failure of the quiz deletion.
    """
    # Call the delete_quiz function to delete the quiz
    delete_quiz_message = delete_quiz(user_id, category_id, session)

    # Return the delete quiz message if available
    if delete_quiz_message:
        return delete_quiz_message

    # Raise a NotFoundException if the quiz is not found
    raise NotFoundException("Quiz")


# =================================================================================================================================
