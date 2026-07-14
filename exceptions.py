class DuplicateDrinkError(Exception):
    """Exception raised when attempting to create a duplicate drink."""

    def __init__(self, message: str):
        super().__init__(message)

class DuplicateCustomerError(Exception):
    """Exception raised when attempting to create a duplicate customer."""

    def __init__(self, message: str):
        super().__init__(message)

class InvalidEmailError(Exception):
    """Exception raised when email validation fails."""

    def __init__(self, message: str):
        super().__init__(message)


