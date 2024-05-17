from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

class Category(SQLModel, table=True):
    """Model for quiz categories."""
    category_id: int | None = Field(None, primary_key=True)
    category_name: str  # Name of the category
    category_description: str  # Description of the category


class Question(SQLModel, table=True):
    """Model for quiz questions."""
    question_id: int | None = Field(None, primary_key=True)
    question: str  # Text of the question
    category_id: int = Field(int, foreign_key="category.category_id")  # ID of the associated category
    choices: list["Choice"] = Relationship(back_populates="question")  # Choices associated with the question


class CategoryQuizDetails(SQLModel, table=True):
    """Model for details of quizzes taken by users in specific categories."""
    id: Optional[int] = Field(None, primary_key=True)
    user_id: int = Field(None, foreign_key="user.user_id")  # ID of the user
    category_id: int = Field(int, foreign_key="category.category_id")  # ID of the category
    obtaining_marks: int = 0  # Marks obtained in the quiz
    percentage: Optional[int] = Field(0, le=100)  # Percentage score
    rank: Optional[str] = None  # Rank achieved
    remaining_questions: int = 10  # Number of remaining questions
    is_finished: bool = False  # Flag indicating if the quiz is finished


class CategoryMarks(SQLModel, table=True):
    """Model for marks obtained in quiz categories."""
    id: Optional[int] = Field(None, primary_key=True)
    category_id: int = Field(int, foreign_key="category.category_id")  # ID of the category
    marks: int = 50  # Marks obtained


class Choice(SQLModel, table=True):
    """Model for choices in quiz questions."""
    choice_id: Optional[int] = Field(None, primary_key=True)
    choice: str  # Text of the choice
    choice_status: bool  # Status of the choice (correct/incorrect)
    question_id: Optional[int] = Field(
        None, foreign_key="question.question_id")  # ID of the associated question
    question: Optional[Question] = Relationship(back_populates="choices")  # Question associated with the choice