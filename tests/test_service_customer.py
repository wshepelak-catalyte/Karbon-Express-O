import pytest
from decimal import Decimal
from models.customer import Customer
from repositories.customer_repository import CustomerRepository
from services.customer_service import CustomerService
from exceptions import DuplicateCustomerError, InvalidEmailFormat

@pytest.fixture
def repo():
    return CustomerRepository()

@pytest.fixture
def service(repo):
    return CustomerService(repo)

@pytest.fixture
def alice():
    return Customer(
        id=1,
        name="Alice",
        email="alice@example.com",
        phone="555-0001",
        username="alice123",
        lifetime_spend=Decimal("0")
    )

@pytest.fixture
def alice_duplicate_email():
    return Customer(
        id=2,
        name="Alicia",
        email="ALICE@example.com",
        phone="555-0002",
        username="alicia123",
        lifetime_spend=Decimal("0")
    )

@pytest.fixture
def alice_duplicate_username():
    return Customer(
        id=3,
        name="Alicia",
        email="alice2@example.com",
        phone="555-0003",
        username="alice123",
        lifetime_spend=Decimal("0")
    )


def test_validate_email_format_accepts_valid_email(service):
    assert service.validate_email_format("user.name+tag@example.com") is True


def test_validate_email_format_rejects_invalid_email(service):
    assert service.validate_email_format("not-an-email") is False
    assert service.validate_email_format("missing@domain") is False
    assert service.validate_email_format("user@domain.c") is False


def test_create_customer_adds_customer_with_valid_data(service, repo, alice):
    created = service.create_customer(alice)
    assert created is alice
    assert repo.get_by_name("Alice") == alice


def test_create_customer_rejects_duplicate_username(service, alice, alice_duplicate_username):
    service.create_customer(alice)
    with pytest.raises(DuplicateCustomerError):
        service.create_customer(alice_duplicate_username)


def test_create_customer_rejects_duplicate_email(service, alice, alice_duplicate_email):
    service.create_customer(alice)
    with pytest.raises(DuplicateCustomerError):
        service.create_customer(alice_duplicate_email)


def test_create_customer_rejects_invalid_email(service):
    customer = Customer(id=3, name="Bob", email="invalid-email", phone="555-1234", username="bob123", lifetime_spend=Decimal("0"))
    with pytest.raises(InvalidEmailFormat) as exc_info:
        service.create_customer(customer)

    assert "Invalid email format" in str(exc_info.value)
    assert "user@example.com" in str(exc_info.value)


def test_create_customer_rejects_duplicate_username_message(service, alice, alice_duplicate_username):
    service.create_customer(alice)
    with pytest.raises(DuplicateCustomerError) as exc_info:
        service.create_customer(alice_duplicate_username)

    assert "already taken" in str(exc_info.value)
    assert "choose a different username" in str(exc_info.value)


def test_create_customer_rejects_duplicate_email_message(service, alice, alice_duplicate_email):
    service.create_customer(alice)
    with pytest.raises(DuplicateCustomerError) as exc_info:
        service.create_customer(alice_duplicate_email)

    assert "already registered" in str(exc_info.value)
    assert "Please use a different email address" in str(exc_info.value)
