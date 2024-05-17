from starlette.config import Config

# Load environment variables from .env file
try:
    config = Config(".env")
except FileNotFoundError:
    print("Environment file (.env) not found")

# Database connection URLs
DB_URL = config.get("DB_CONNECTION_STR")
TEST_DB_URL = config.get("TEST_DB_CONNECTION_STR")

# OPENAPI KEY
OPEN_AI_KEY = config.get("OPEN_AI_KEY")