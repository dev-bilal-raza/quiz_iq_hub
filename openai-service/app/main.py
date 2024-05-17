from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils.apierrors import ConflictsException, InvalidInputException, NotFoundException
from app.config.database import create_table, DB_SESSION
from app.controllers.openai_controller import generate_question, openai_conversation


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
app = FastAPI(title="QuizIQHub", lifespan=lifespan)


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


class PromptModel(BaseModel):
    user_id: int
    message: str


@app.get("/", response_model=dict[str, str])
def userHome():

    return {
        "service": "user-service",
        "message": ""
    }


@app.get("/api/generate_mcqs")
async def generateMcqs(category: int, session: DB_SESSION):
    openAi_mcq = generate_question(category=category, session=session)
    if not openAi_mcq:
        raise NotImplementedError("MCQ could not be generated")
    return openAi_mcq


@app.get("/api/conversation")
def conversation(prompt: PromptModel):
    if prompt.user_id and prompt.message:
        response = openai_conversation(str(prompt))
        return response
    raise NotImplementedError("You have not implemented any prompt yet.")
