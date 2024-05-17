from typing import Any
from starlette.config import Config
from datetime import timedelta
import os
# Load environment variables from .env file
try:
    config = Config(".env")
except FileNotFoundError:
    print("Environment file (.env) not found")

# Database connection URLs
DB_URL = os.getenv("DB_CONNECTION_STR")
TEST_DB_URL = os.getenv("TEST_DB_CONNECTION_STR")

# JWT settings
ALGORITHM = config.get("ALGORITHM")
SECRET_KEY = config.get("SECRET_KEY")

access_time: Any = config.get("ACCESS_TOKEN_EXPIRE_TIME")
refresh_time: Any = config.get("ACCESS_TOKEN_EXPIRE_TIME")
admin_time: Any = config.get("ACCESS_TOKEN_EXPIRE_TIME")
# print(access_time)

# Token expiration times
ACCESS_TOKEN_EXPIRE_TIME = timedelta(minutes=int(access_time))
REFRESH_TOKEN_EXPIRE_TIME = timedelta(days=int(refresh_time))
