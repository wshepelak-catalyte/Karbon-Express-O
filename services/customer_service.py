from repositories.customer_repository import CustomerRepository
from models.customer import Customer


class CustomerService:
    """Service layer for customer operations."""

    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

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
