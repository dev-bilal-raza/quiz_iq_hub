from typing import Optional
from sqlmodel import SQLModel, Field
from quizbackend.utils.types import ChoiceType
from pydantic import BaseModel

class AdminBaseModel(SQLModel):
    """Base model for admin."""
    admin_email: str
    admin_password: str

class Admin(AdminBaseModel, table=True):
    """Model for admin with primary key."""
    id: Optional[int] = Field(None, primary_key=True)

class AdminToken(SQLModel, table=True):
    """Model for admin token."""
    admin_tokenId: Optional[int] = Field(None, primary_key=True)
    admin_token: str

class QuestionModel(BaseModel):
    """Model for quiz question."""
    question: str  # Question text
    category_id: int  # Category ID for the question
    choice1: ChoiceType  # Choice 1
    choice2: ChoiceType  # Choice 2
    choice3: ChoiceType  # Choice 3
    choice4: ChoiceType  # Choice 4

class CategoryModel(BaseModel):
    """Model for quiz category."""
    category: str  # Category name
    category_description: str  # Category description
    category_marks: Optional[int]  # Category marks (if applicable)
