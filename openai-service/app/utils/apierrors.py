class NotFoundException(Exception):
    """Exception raised when the requested resource is not found."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class InvalidInputException(Exception):
    """Exception raised when the input data is invalid."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class ConflictsException(Exception):
    """Exception raised when there are conflicts with existing data."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
