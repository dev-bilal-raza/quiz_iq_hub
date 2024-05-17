from passlib.context import CryptContext

# Password context for hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===============================================================================================================================
def passwordIntoHash(password: str) -> str:
    """
    Hashes the provided password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    hash_password = pwd_context.hash(password)
    return hash_password


# ===============================================================================================================================
def verifyPassword(plainText: str, hashedPassword: str) -> bool:
    """
    Verifies if the provided plaintext password matches the hashed password.

    Args:
        plainText (str): The plaintext password.
        hashedPassword (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    # Print the plaintext and hashed passwords for debugging
    print(plainText, hashedPassword)

    # Verify if the plaintext password matches the hashed password
    isPasswordCorrect = pwd_context.verify(plainText, hash=hashedPassword)

    # Print the result of password verification for debugging
    print(isPasswordCorrect)

    return isPasswordCorrect
