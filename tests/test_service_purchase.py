import pytest
from datetime import datetime, timezone
from decimal import Decimal
from models.customer import Customer
from repositories.purchase_repository import PurchaseRepository
from services.purchase_service import PurchaseService
from exceptions import PurchaseIdNotFound

@pytest.fixture
def purchase_repo():
    return PurchaseRepository()

@pytest.fixture
def service(purchase_repo):
    return PurchaseService(purchase_repo)

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

def test_create_purchase_adds_purchase(service, customer):
    service.create_purchase(
        timestamp=datetime.now(timezone.utc),
        items=["Coffee"],
        total_cost=Decimal("15.50"),
        customer=customer,
    )

    purchases = service.get_all_purchases()
    assert len(purchases) == 1
    assert purchases[0].customer.username == "alice123"
    assert purchases[0].total_cost == Decimal("15.50")


def test_get_purchase_by_id_returns_matching_purchase(service, customer):
    service.create_purchase(
        timestamp=datetime.now(timezone.utc),
        items=["Coffee"],
        total_cost=Decimal("15.50"),
        customer=customer,
    )

    purchase = service.get_purchase_by_id(0)
    assert purchase.customer.username == "alice123"
    assert purchase.total_cost == Decimal("15.50")


def test_get_purchase_by_id_raises_when_missing(service):
    with pytest.raises(PurchaseIdNotFound):
        service.get_purchase_by_id(999)


def test_get_total_spending_sums_all_purchase_totals(service, customer):
    service.create_purchase(
        timestamp=datetime.now(timezone.utc),
        items=["Coffee"],
        total_cost=Decimal("15.50"),
        customer=customer,
    )
    service.create_purchase(
        timestamp=datetime.now(timezone.utc),
        items=["Bagel"],
        total_cost=Decimal("4.50"),
        customer=customer,
    )

    assert service.get_total_spending() == Decimal("20.00")
