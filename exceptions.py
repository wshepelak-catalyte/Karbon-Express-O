class DuplicateDrinkError(Exception):
    """Exception raised when attempting to create a duplicate drink."""

    def __init__(self, message: str):
        super().__init__(message)

class DrinkNotFoundError(Exception):       
    """Exception raised when a drink is not found in the repository."""

    def __init__(self, message: str):
        super().__init__(message)

class DuplicateCustomerError(Exception):
    """Exception raised when attempting to create a duplicate customer."""

    def __init__(self, message: str):
        super().__init__(message)

class CustomerNotFoundError(Exception):
    """Exception raised when a customer is not found in the repository"""

    def __init__(self, message : str):
        super().__init__(message)

class InvalidEmailFormat(Exception):
    """Exception raised when a provided email does not match the proper format."""

    def __init__(self, message : str):
        super().__init__(message)

class DuplicatebakedgoodError(Exception):
    """Exception raised when attempting to create a duplicate baked good."""

    def __init__(self, message: str):
        super().__init__(message)

class BakedGoodNotFoundError(Exception):
    """Exception raised when a baked good is not found in the repository."""

    def __init__(self, message : str):
        super().__init__(message)

class DuplicateIngredientError(Exception):
    """Exception raised when attempting to create a duplicate ingredient."""

    def __init__(self, message: str):
        super().__init__(message)

class IngredientNotFound(Exception):
    """Exception raised when an ingredient is not found in the repository."""

    def __init__(self, message : str):
        super().__init__(message)