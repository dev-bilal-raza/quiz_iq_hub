from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    user_id: int | None = Field(int, primary_key=True)
    user_name: str
    user_email: str
    user_password: str
    total_points: int
    