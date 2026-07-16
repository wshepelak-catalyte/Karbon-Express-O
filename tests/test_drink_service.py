from decimal import Decimal

from models.ingredient import Ingredient
from services.drink_service import DrinkService


def make_ingredient() -> Ingredient:
    return Ingredient(
        id=1,
        name="Sugar",
        purchasing_cost=1.0,
        unit_amount=1.0,
        unit_of_measure="cup",
        available=True,
    )


def test_name_duplicate_validation_detects_existing_name():
    service = DrinkService()
    service.create_drink(
        name="Latte",
        ingredients=[make_ingredient()],
        cost_to_produce=Decimal("2.00"),
        markup_percentage=Decimal("0.25"),
        sale_price=Decimal("2.50"),
    )

    assert service.is_name_taken("Latte") is True
    assert service.is_name_taken("latte") is True


def test_name_duplicate_validation_ignores_same_drink_when_updating():
    service = DrinkService()
    service.create_drink(
        name="Latte",
        ingredients=[make_ingredient()],
        cost_to_produce=Decimal("2.00"),
        markup_percentage=Decimal("0.25"),
        sale_price=Decimal("2.50"),
    )
    latte = service.get_drink_by_name("Latte")

    assert service.is_name_taken("Latte", exclude_id=latte.id) is False
    assert service.is_name_taken("Mocha") is False
