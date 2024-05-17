from pydantic import BaseModel

class QuizAttemptModel(BaseModel):
    user_id: int
    category_id: int
    quiz_numbers: int
    isFinished: bool = False

class GetQuizDetailsModel(BaseModel):
    user_id: int
    category_name: str  
    