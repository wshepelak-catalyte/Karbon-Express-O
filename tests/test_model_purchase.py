from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock
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
        timestamp=datetime.now(),
        items=[mock_item],
        total_cost=Decimal("15.50"),
        customer=mock_customer
    )


@pytest.mark.parametrize(
    "total_cost",
    [
        Decimal("4.50"),
        Decimal("12.00"),
        Decimal("0.00"),
    ]
)
def test_purchase_timestamp_initialization(mock_customer, mock_item, total_cost):
    timestamp = datetime.now()
    purchase = Purchase(timestamp, [mock_item], total_cost, mock_customer)
    assert isinstance(purchase.timestamp, datetime)


@pytest.mark.parametrize(
    "total_cost",
    [
        Decimal("4.50"),
        Decimal("12.00"),
        Decimal("0.00"),
    ]
)
def test_purchase_items_initialization(mock_customer, mock_item, total_cost):
    timestamp = datetime.now()
    items = [mock_item]
    purchase = Purchase(timestamp, items, total_cost, mock_customer)
    assert purchase.items == items


@pytest.mark.parametrize(
    "total_cost",
    [
        Decimal("4.50"),
        Decimal("12.00"),
        Decimal("0.00"),
    ]
)
def test_purchase_total_cost_initialization(mock_customer, mock_item, total_cost):
    timestamp = datetime.now()
    purchase = Purchase(timestamp, [mock_item], total_cost, mock_customer)
    assert purchase.total_cost == total_cost


@pytest.mark.parametrize(
    "total_cost",
    [
        Decimal("4.50"),
        Decimal("12.00"),
        Decimal("0.00"),
    ]
)
def test_purchase_customer_initialization(mock_customer, mock_item, total_cost):
    timestamp = datetime.now()
    purchase = Purchase(timestamp, [mock_item], total_cost, mock_customer)
    assert purchase.customer == mock_customer


def test_purchase_equality_with_identical_attributes(mock_customer, mock_item):
    timestamp = datetime.now()
    purchase_one = Purchase(timestamp, [mock_item], Decimal("5.00"), mock_customer)
    purchase_two = Purchase(timestamp, [mock_item], Decimal("5.00"), mock_customer)
    assert purchase_one == purchase_two


def test_purchase_inequality_with_different_total_costs(mock_customer, mock_item):
    timestamp = datetime.now()
    purchase_one = Purchase(timestamp, [mock_item], Decimal("5.00"), mock_customer)
    purchase_two = Purchase(timestamp, [mock_item], Decimal("6.00"), mock_customer)
    assert purchase_one != purchase_two


@pytest.mark.parametrize(
    "attribute_name, mutated_value",
    [
        ("items", []),
        ("total_cost", Decimal("22.75")),
    ]
)
def test_purchase_mutability_after_initialization(valid_purchase, attribute_name, mutated_value):
    setattr(valid_purchase, attribute_name, mutated_value)
    assert getattr(valid_purchase, attribute_name) == mutated_value


def test_purchase_timestamp_attribute_type_is_datetime(valid_purchase):
    assert isinstance(valid_purchase.timestamp, datetime)


def test_purchase_items_attribute_type_is_list(valid_purchase):
    assert isinstance(valid_purchase.items, list)


def test_purchase_total_cost_attribute_type_is_decimal(valid_purchase):
    assert isinstance(valid_purchase.total_cost, Decimal)