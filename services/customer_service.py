import re
from repositories.customer_repository import CustomerRepository

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]{1,30}@[A-Za-z0-9.-]{1,30}\.[A-Za-z]{2,15}$")

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]{1,30}@[A-Za-z0-9.-]{1,30}+\.[A-Za-z]{2,15}$")

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def validate_email_format(self, email: str) -> bool:
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
