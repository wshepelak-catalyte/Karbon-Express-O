from models.customer import Customer
from repositories.customer_repository import CustomerRepository
from services.customer_service import CustomerService


def test_email_duplicate_validation_detects_existing_email():
    repository = CustomerRepository()
    service = CustomerService(repository)
    repository.add(Customer(id=1, name="Alice", email="alice@example.com", lifetime_spend=10.0))

    assert service.is_email_taken("alice@example.com") is True
    assert service.is_email_taken("ALICE@example.com") is True


def test_email_duplicate_validation_ignores_same_customer_when_updating():
    repository = CustomerRepository()
    service = CustomerService(repository)
    repository.add(Customer(id=1, name="Alice", email="alice@example.com", lifetime_spend=10.0))

    assert service.is_email_taken("alice@example.com", exclude_id=1) is False
    assert service.is_email_taken("bob@example.com") is False
