from decimal import Decimal
from unittest.mock import Mock
import pytest
from models.drink import Drink
from repositories.drink_repository import DrinkRepository

@pytest.fixture
def repo():
    return DrinkRepository()

@pytest.fixture
def mock_ingredient():
    return Mock()

@pytest.fixture
def espresso(mock_ingredient):
    return Drink(
        id=1,
        name="Espresso",
        ingredients=[mock_ingredient],
        cost_to_produce=Decimal("0.50"),
        markup_percentage=Decimal("3.0"),
        sale_price=Decimal("2.00")
    )

@pytest.fixture
def latte(mock_ingredient):
    return Drink(
        id=2,
        name="Latte",
        ingredients=[mock_ingredient],
        cost_to_produce=Decimal("0.80"),
        markup_percentage=Decimal("2.5"),
        sale_price=Decimal("2.80")
    )

def test_get_all_initially_returns_empty_list(repo):
    assert repo.get_all() == []

def test_add_appends_drink_to_repository(repo, espresso):
    repo.add(espresso)
    assert repo.get_all() == [espresso]

def test_add_returns_the_added_drink(repo, espresso):
    returned_drink = repo.add(espresso)
    assert returned_drink == espresso

def test_get_by_id_returns_matching_drink(repo, espresso, latte):
    repo.add(espresso)
    repo.add(latte)
    assert repo.get_by_id(2) == latte

def test_get_by_id_returns_none_when_not_found(repo, espresso):
    repo.add(espresso)
    assert repo.get_by_id(999) is None

def test_update_replaces_existing_drink(repo, espresso, latte):
    repo.add(espresso)
    repo.update(1, latte)
    assert repo.get_all() == [latte]

def test_update_returns_new_drink_on_success(repo, espresso, latte):
    repo.add(espresso)
    returned_drink = repo.update(1, latte)
    assert returned_drink == latte

def test_update_returns_none_when_target_missing(repo, espresso, latte):
    repo.add(espresso)
    returned_value = repo.update(999, latte)
    assert returned_value is None

def test_update_does_not_modify_list_when_target_missing(repo, espresso, latte):
    repo.add(espresso)
    repo.update(999, latte)
    assert repo.get_all() == [espresso]

def test_delete_removes_drink_from_repository(repo, espresso, latte):
    repo.add(espresso)
    repo.add(latte)
    repo.delete(1)
    assert repo.get_all() == [latte]

def test_delete_returns_true_on_success(repo, espresso):
    repo.add(espresso)
    assert repo.delete(1) is True

def test_delete_returns_false_when_target_missing(repo, espresso):
    repo.add(espresso)
    assert repo.delete(999) is False


def test_get_by_name_returns_matching_drink_case_insensitive(repo, espresso, latte):
    repo.add(espresso)
    repo.add(latte)
    assert repo.get_by_name("espresso") == espresso
    assert repo.get_by_name(" LATTE ") == latte


def test_get_by_name_returns_none_when_not_found(repo, espresso):
    repo.add(espresso)
    assert repo.get_by_name("Cappuccino") is None