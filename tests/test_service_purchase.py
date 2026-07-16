import pytest
from datetime import datetime, timezone
from decimal import Decimal
from models.purchase import Purchase
from models.customer import Customer
from repositories.purchase_repository import PurchaseRepository
from repositories.customer_repository import CustomerRepository
from services.purchase_service import PurchaseService

@pytest.fixture
def customer_repo():
    return CustomerRepository()

@pytest.fixture
def purchase_repo():
    return PurchaseRepository()

@pytest.fixture
def service(purchase_repo, customer_repo):
    return PurchaseService(purchase_repo, customer_repo)

@pytest.fixture
def customer():
    return Customer(
        id=1,
        name="Alice",
        email="alice@example.com",
        phone="555-0001",
        username="alice123",
        lifetime_spend=Decimal("0")
    )

@pytest.fixture
def purchase(customer):
    return Purchase(
        id=1,
        timestamp=datetime.now(timezone.utc),
        items=["Coffee"],
        total_cost=Decimal("15.50"),
        customer=customer
    )

def test_add_purchase_links_to_customer(service, customer_repo, customer, purchase):
    customer_repo.add(customer)

    created = service.add_purchase(purchase)

    assert created == purchase
    assert len(customer.purchases) == 1
    assert customer.purchases[0] == purchase
    assert customer.lifetime_spend == Decimal("15.50")

def test_get_customer_purchase_history_returns_customer_purchases(service, customer_repo, customer, purchase):
    customer_repo.add(customer)
    service.add_purchase(purchase)

    history = service.get_customer_purchase_history("alice123")

    assert history == [purchase]

def test_get_customer_purchase_history_for_missing_customer_returns_empty_list(service):
    history = service.get_customer_purchase_history("missing")

    assert history == []

def test_add_purchase_raises_if_customer_missing(service, purchase):
    with pytest.raises(ValueError):
        service.add_purchase(purchase)
