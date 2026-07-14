from decimal import Decimal
from unittest.mock import Mock
import pytest
from models.drink import Drink
from repositories.drink_repository import DrinkRepository
from services.drink_service import DrinkService
from exceptions import DuplicateDrinkError

@pytest.fixture
def repo():
    return DrinkRepository()

@pytest.fixture
def service(repo):
    return DrinkService(repo)

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
def duplicate_espresso(mock_ingredient):
    return Drink(
        id=2,
        name="espresso",
        ingredients=[mock_ingredient],
        cost_to_produce=Decimal("0.60"),
        markup_percentage=Decimal("2.0"),
        sale_price=Decimal("2.40")
    )


def test_create_drink_allows_unique_name(service, espresso):
    created = service.create_drink(espresso)
    assert created == espresso


def test_create_drink_raises_duplicate_error_for_same_name(service, espresso, duplicate_espresso):
    service.create_drink(espresso)

    with pytest.raises(DuplicateDrinkError) as exc_info:
        service.create_drink(duplicate_espresso)

    assert "Drink 'espresso' already exists." in str(exc_info.value)
