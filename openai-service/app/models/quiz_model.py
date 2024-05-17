from sqlmodel import SQLModel, Field
from typing import Optional

class Category(SQLModel, table=True):
    """Model for quiz categories."""
    category_id: int | None = Field(None, primary_key=True)
    category_name: str  # Name of the category
    category_description: str  # Description of the category

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
