from decimal import Decimal
from unittest.mock import Mock
import pytest
from models.drink import Drink
from services.drink_service import DrinkService
from exceptions import DuplicateDrinkError

@pytest.fixture
def service():
    return DrinkService()

@pytest.fixture
def mock_ingredient():
    return Mock()

def test_create_drink_allows_unique_name(service, mock_ingredient):
    service.create_drink(
        name="Espresso",
        ingredients=[mock_ingredient],
        cost_to_produce=Decimal("0.50"),
        markup_percentage=Decimal("3.0"),
        sale_price=Decimal("2.00"),
        is_available=True
    )
    all_drinks = service.get_all_drinks()
    assert len(all_drinks) == 1
    assert all_drinks[0].name == "Espresso"

def test_create_drink_raises_duplicate_error_for_exact_name_match(service, mock_ingredient):
    service.create_drink(
        name="Espresso",
        ingredients=[mock_ingredient],
        cost_to_produce=Decimal("0.50"),
        markup_percentage=Decimal("3.0"),
        sale_price=Decimal("2.00")
    )
    with pytest.raises(DuplicateDrinkError) as exc_info:
        service.create_drink(
            name="Espresso",
            ingredients=[mock_ingredient],
            cost_to_produce=Decimal("0.60"),
            markup_percentage=Decimal("2.0"),
            sale_price=Decimal("2.40")
        )
    assert "Drink 'Espresso' already exists." in str(exc_info.value)