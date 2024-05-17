from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    """Base model for user."""
    user_email: str  # Email of the user
    user_password: str  # Password of the user


class UserLogInModel(UserBase):
    """Model for user login."""
    pass

class UserSignUpModel(UserBase):
    """Model for user sign-up."""
    user_name: str  # Name of the user

class UpdateUserModel(SQLModel):
    """Model for user sign-up."""
    user_id: int
    user_name: str # Name of the user
    user_email: str  # Name of the user

class User(UserSignUpModel, table=True):
    """Model for registered users."""
    user_id: int | None = Field(None, primary_key=True)  # ID of the user
    total_points: int = 0  # Total points accumulated by the user


class Token(SQLModel, table=True):
    """Model for user tokens."""
    id: int | None = Field(None, primary_key=True)  # Token ID
    user_id: int  # ID of the associated user
    refresh_token: str  # Refresh token