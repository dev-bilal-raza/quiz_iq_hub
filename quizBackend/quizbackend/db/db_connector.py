from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session
from quizbackend.settings import DB_URL, TEST_DB_URL
from fastapi import Depends

# Replace part of database connection strings
db_connection_str = str(DB_URL).replace("postgresql", "postqresql+psycopg")
test_db_connection_str = str(TEST_DB_URL).replace(
    "postgresql", "postqresql+psycopg")

# Create database engine
db_engine = create_engine(db_connection_str, pool_pre_ping=True, connect_args={
    "sslmode": "require"
}, pool_recycle=600)

def create_table():
    """Creates tables in the database."""
    print("Creating Tables...")
    SQLModel.metadata.create_all(db_engine)

def get_session():
    """Returns a database session."""
    with Session(db_engine) as session:
        yield session

# Annotate dependency for database session
DB_SESSION = Annotated[Session, Depends(get_session)]
