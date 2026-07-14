import re
from dataclasses import dataclass
from repositories.customer_repository import CustomerRepository

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]{1,30}@[A-Za-z0-9.-]{1,30}\.[A-Za-z]{2,15}$")

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def validate_email_format(self, email: str) -> bool:
        """Validates that customer email follows a proper format"""
        return re.fullmatch(EMAIL_PATTERN, email) is not None

    def is_email_taken(self, email: str, exclude_id: int | None = None) -> bool:
        """Return True when another customer already uses the same email."""
        normalized_email = email.strip().lower()
        for customer in self.repository.get_all():
            if customer.email.lower() != normalized_email:
                continue
            if exclude_id is not None and customer.id == exclude_id:
                continue
            return True
        return False
from models.customer import Customer
from exceptions import DuplicateCustomerError, InvalidEmailError

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]{1,30}@[A-Za-z0-9.-]{1,30}\.[A-Za-z]{2,15}$")

@dataclass
class ValidationResult:
    valid: bool
    code: str | None = None
    message: str | None = None

class CustomerService:
    def __init__(self, repository : CustomerRepository):
        self._repository = repository

    def validate_email_format(self, email : str) -> bool:
        return re.fullmatch(EMAIL_PATTERN, email.strip()) is not None

    def is_unique_username(self, username: str) -> bool:
        return self._repository.get_by_username(username) is None

    def is_unique_email(self, email: str) -> bool:
        return self._repository.get_by_email(email) is None

    def validate_customer_signup(self, customer: Customer) -> ValidationResult:
        if not self.validate_email_format(customer.email):
            return ValidationResult(
                valid=False,
                code="invalid_email",
                message="Invalid email format. Please use a valid email address like user@example.com."
            )

        if not self.is_unique_username(customer.username):
            return ValidationResult(
                valid=False,
                code="duplicate_username",
                message=f"Username '{customer.username}' is already taken. Please choose a different username."
            )

        if not self.is_unique_email(customer.email):
            return ValidationResult(
                valid=False,
                code="duplicate_email",
                message=f"Email '{customer.email}' is already registered. Please use a different email address."
            )

        return ValidationResult(valid=True)

    def create_customer(self, customer: Customer) -> Customer:
        validation = self.validate_customer_signup(customer)
        if not validation.valid:
            if validation.code == "invalid_email":
                raise InvalidEmailError(validation.message)
            if validation.code in {"duplicate_username", "duplicate_email"}:
                raise DuplicateCustomerError(validation.message)
            raise ValueError(validation.message or "Invalid customer signup data.")

        return self._repository.add(customer)
