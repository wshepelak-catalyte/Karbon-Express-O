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

class DuplicateUsernameError(Exception):
    """Exception raised when attempting to create a duplicate username."""

    def __init__(self, message: str):
        super().__init__(message)

class DuplicatebakedgoodError(Exception):
    """Exception raised when attempting to create a duplicate baked good."""

    def __init__(self, message: str):
        super().__init__(message)

class DuplicateIngredientError(Exception):
    """Exception raised when attempting to create a duplicate ingredient."""

    def __init__(self, message: str):
        super().__init__(message)

class ItemNotFoundError(Exception):
    """Exception raised when an item is not found in the repository."""

    def __init__(self, message: str):
        super().__init__(message)

        
