from decimal import Decimal

from models.drink import Drink
from models.ingredient import Ingredient
from repositories.drink_repository import DrinkRepository
from services.drink_service import DrinkService


def make_drink(id_value: int, name: str) -> Drink:
    ingredient = Ingredient(id=1, name="Sugar", purchasing_cost=1.0, unit_amount=1.0, unit_of_measure="cup")
    return Drink(
        id=id_value,
        name=name,
        ingredients=[ingredient],
        cost_to_produce=Decimal("2.00"),
        markup_percentage=Decimal("0.25"),
        sale_price=Decimal("0"),
    )


def test_name_duplicate_validation_detects_existing_name():
    repository = DrinkRepository()
    service = DrinkService(repository)
    repository.add(make_drink(1, "Latte"))

    assert service.is_name_taken("Latte") is True
    assert service.is_name_taken("latte") is True


def test_name_duplicate_validation_ignores_same_drink_when_updating():
    repository = DrinkRepository()
    service = DrinkService(repository)
    repository.add(make_drink(1, "Latte"))

    assert service.is_name_taken("Latte", exclude_id=1) is False
    assert service.is_name_taken("Mocha") is False
