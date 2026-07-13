from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch
import pytest
from models.purchase import Purchase

@pytest.fixture
def mock_customer():
    return Mock()

@pytest.fixture
def mock_item():
    return Mock()

@pytest.fixture
def valid_purchase(mock_customer, mock_item):
    return Purchase(
        id=1,
        timestamp=datetime.now(timezone.utc),
        items=[mock_item],
        total_cost=Decimal("15.50"),
        customer=mock_customer
    )

@pytest.mark.parametrize(
    "id, total_cost",
    [
        (1, Decimal("4.50")),
        (2, Decimal("12.00")),
        (3, Decimal("0.00")),
    ]
)
def test_purchase_id_initialization(mock_customer, mock_item, id, total_cost):
    timestamp = datetime.now(timezone.utc)
    purchase = Purchase(id=id, timestamp=timestamp, items=[mock_item], total_cost=total_cost, customer=mock_customer)
    assert purchase.id == id

@pytest.mark.parametrize(
    "id, total_cost",
    [
        (1, Decimal("4.50")),
        (2, Decimal("12.00")),
        (3, Decimal("0.00")),
    ]
)
def test_purchase_timestamp_initialization(mock_customer, mock_item, id, total_cost):
    timestamp = datetime.now(timezone.utc)
    purchase = Purchase(id=id, timestamp=timestamp, items=[mock_item], total_cost=total_cost, customer=mock_customer)
    assert isinstance(purchase.timestamp, datetime)

@pytest.mark.parametrize(
    "id, total_cost",
    [
        (1, Decimal("4.50")),
        (2, Decimal("12.00")),
        (3, Decimal("0.00")),
    ]
)
def test_purchase_items_initialization(mock_customer, mock_item, id, total_cost):
    timestamp = datetime.now(timezone.utc)
    items = [mock_item]
    purchase = Purchase(id=id, timestamp=timestamp, items=items, total_cost=total_cost, customer=mock_customer)
    assert purchase.items == items

@pytest.mark.parametrize(
    "id, total_cost",
    [
        (1, Decimal("4.50")),
        (2, Decimal("12.00")),
        (3, Decimal("0.00")),
    ]
)
def test_purchase_total_cost_initialization(mock_customer, mock_item, id, total_cost):
    timestamp = datetime.now(timezone.utc)
    purchase = Purchase(id=id, timestamp=timestamp, items=[mock_item], total_cost=total_cost, customer=mock_customer)
    assert purchase.total_cost == total_cost

@pytest.mark.parametrize(
    "id, total_cost",
    [
        (1, Decimal("4.50")),
        (2, Decimal("12.00")),
        (3, Decimal("0.00")),
    ]
)
def test_purchase_customer_initialization(mock_customer, mock_item, id, total_cost):
    timestamp = datetime.now(timezone.utc)
    purchase = Purchase(id=id, timestamp=timestamp, items=[mock_item], total_cost=total_cost, customer=mock_customer)
    assert purchase.customer == mock_customer

def test_purchase_equality_with_identical_attributes(mock_customer, mock_item):
    fixed_time = datetime(2026, 7, 13, 12, 0, 0, tzinfo=timezone.utc)
    with patch("models.purchase.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        purchase_one = Purchase(id=1, timestamp=fixed_time, items=[mock_item], total_cost=Decimal("5.00"), customer=mock_customer)
        purchase_two = Purchase(id=1, timestamp=fixed_time, items=[mock_item], total_cost=Decimal("5.00"), customer=mock_customer)
        assert purchase_one == purchase_two

def test_purchase_inequality_with_different_ids(mock_customer, mock_item):
    timestamp = datetime.now(timezone.utc)
    purchase_one = Purchase(id=1, timestamp=timestamp, items=[mock_item], total_cost=Decimal("5.00"), customer=mock_customer)
    purchase_two = Purchase(id=2, timestamp=timestamp, items=[mock_item], total_cost=Decimal("5.00"), customer=mock_customer)
    assert purchase_one != purchase_two

def test_purchase_inequality_with_different_total_costs(mock_customer, mock_item):
    timestamp = datetime.now(timezone.utc)
    purchase_one = Purchase(id=1, timestamp=timestamp, items=[mock_item], total_cost=Decimal("5.00"), customer=mock_customer)
    purchase_two = Purchase(id=1, timestamp=timestamp, items=[mock_item], total_cost=Decimal("6.00"), customer=mock_customer)
    assert purchase_one != purchase_two

@pytest.mark.parametrize(
    "attribute_name, mutated_value",
    [
        ("id", 9),
        ("items", []),
        ("total_cost", Decimal("22.75")),
    ]
)
def test_purchase_mutability_after_initialization(valid_purchase, attribute_name, mutated_value):
    setattr(valid_purchase, attribute_name, mutated_value)
    assert getattr(valid_purchase, attribute_name) == mutated_value

def test_purchase_id_attribute_type_is_int(valid_purchase):
    assert isinstance(valid_purchase.id, int)

def test_purchase_timestamp_attribute_type_is_datetime(valid_purchase):
    assert isinstance(valid_purchase.timestamp, datetime)

def test_purchase_items_attribute_type_is_list(valid_purchase):
    assert isinstance(valid_purchase.items, list)

def test_purchase_total_cost_attribute_type_is_decimal(valid_purchase):
    assert isinstance(valid_purchase.total_cost, Decimal)