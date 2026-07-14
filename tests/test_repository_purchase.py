from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock
import pytest
from models.purchase import Purchase
from repositories.purchase_repository import PurchaseRepository

@pytest.fixture
def repo():
    return PurchaseRepository()

@pytest.fixture
def mock_customer():
    return Mock()

@pytest.fixture
def mock_item():
    return Mock()

@pytest.fixture
def purchase_one(mock_customer, mock_item):
    return Purchase(
        id=1,
        timestamp=datetime.now(timezone.utc),
        items=[mock_item],
        total_cost=Decimal("15.50"),
        customer=mock_customer
    )

@pytest.fixture
def purchase_two(mock_customer, mock_item):
    return Purchase(
        id=2,
        timestamp=datetime.now(timezone.utc),
        items=[mock_item],
        total_cost=Decimal("24.00"),
        customer=mock_customer
    )

def test_get_all_initially_returns_empty_list(repo):
    assert repo.get_all() == []

def test_add_appends_purchase_to_repository(repo, purchase_one):
    repo.add(purchase_one)
    assert repo.get_all() == [purchase_one]

def test_add_returns_the_added_purchase(repo, purchase_one):
    returned_purchase = repo.add(purchase_one)
    assert returned_purchase == purchase_one

def test_get_by_id_returns_matching_purchase(repo, purchase_one, purchase_two):
    repo.add(purchase_one)
    repo.add(purchase_two)
    assert repo.get_by_id(2) == purchase_two

def test_get_by_id_returns_none_when_not_found(repo, purchase_one):
    repo.add(purchase_one)
    assert repo.get_by_id(999) is None

def test_update_replaces_existing_purchase(repo, purchase_one, purchase_two):
    repo.add(purchase_one)
    repo.update(1, purchase_two)
    assert repo.get_all() == [purchase_two]

def test_update_returns_new_purchase_on_success(repo, purchase_one, purchase_two):
    repo.add(purchase_one)
    returned_purchase = repo.update(1, purchase_two)
    assert returned_purchase == purchase_two

def test_update_returns_none_when_target_missing(repo, purchase_one, purchase_two):
    repo.add(purchase_one)
    returned_value = repo.update(999, purchase_two)
    assert returned_value is None

def test_update_does_not_modify_list_when_target_missing(repo, purchase_one, purchase_two):
    repo.add(purchase_one)
    repo.update(999, purchase_two)
    assert repo.get_all() == [purchase_one]