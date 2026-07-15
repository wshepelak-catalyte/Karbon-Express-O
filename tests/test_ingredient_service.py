from decimal import Decimal

from models.drink import Drink
from models.ingredient import Ingredient
from repositories.drink_repository import DrinkRepository
from repositories.ingredient_availability_repository import IngredientAvailabilityRepository
from repositories.ingredient_repository import IngredientRepository
from services.ingredient_service import IngredientService


def test_mark_unavailable_disables_drinks_that_depend_on_it():
    ingredient_repo = IngredientRepository()
    availability_repo = IngredientAvailabilityRepository()
    drink_repo = DrinkRepository()
    service = IngredientService(ingredient_repo, availability_repo, drink_repo)

    milk = Ingredient(id=1, name="Milk", purchasing_cost=1.0, unit_amount=1.0, unit_of_measure="liter")
    sugar = Ingredient(id=2, name="Sugar", purchasing_cost=0.5, unit_amount=1.0, unit_of_measure="kg")
    service.add_ingredient(milk)
    service.add_ingredient(sugar)

    drink = Drink(
        id=1,
        name="Latte",
        ingredients=[milk, sugar],
        cost_to_produce=Decimal("2.00"),
        markup_percentage=Decimal("0.25"),
        sale_price=Decimal("0"),
    )
    drink_repo.add(drink)

    service.mark_unavailable("Sugar")

    assert service.is_drink_available(1) is False
    assert drink.is_available is False


def test_mark_available_re_enables_drinks_when_ingredient_returns():
    ingredient_repo = IngredientRepository()
    availability_repo = IngredientAvailabilityRepository()
    drink_repo = DrinkRepository()
    service = IngredientService(ingredient_repo, availability_repo, drink_repo)

    milk = Ingredient(id=1, name="Milk", purchasing_cost=1.0, unit_amount=1.0, unit_of_measure="liter")
    sugar = Ingredient(id=2, name="Sugar", purchasing_cost=0.5, unit_amount=1.0, unit_of_measure="kg")
    service.add_ingredient(milk)
    service.add_ingredient(sugar)

    drink = Drink(
        id=2,
        name="Latte",
        ingredients=[milk, sugar],
        cost_to_produce=Decimal("2.00"),
        markup_percentage=Decimal("0.25"),
        sale_price=Decimal("0"),
    )
    drink_repo.add(drink)

    service.mark_unavailable("Sugar")
    service.mark_available("Sugar")

    assert service.is_drink_available(2) is True
    assert drink.is_available is True
