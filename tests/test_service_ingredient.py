import pytest
from decimal import Decimal
from models.ingredient import Ingredient
from services.ingredient_service import IngredientService
from exceptions import DuplicateIngredientError, IngredientNotFound


@pytest.fixture
def service():
    return IngredientService()


def test_create_ingredient_adds_ingredient_to_repository(service):
    """Ensure creating an ingredient stores it in the repository."""
    created = service.create_ingredient(
        name="Milk",
        purchasing_cost=Decimal("3.50"),
        unit_amount=1.0,
        unit_of_measure="liter",
        available=True,
    )

    assert created is None
    assert len(service.get_all_ingredients()) == 1
    stored_ingredient = service.get_all_ingredients()[0]
    assert stored_ingredient.name == "Milk"
    assert stored_ingredient.purchasing_cost == Decimal("3.50")
    assert stored_ingredient.available is True


def test_create_ingredient_rejects_duplicate_name(service):
    """Ensure duplicate ingredient names are rejected."""
    service.create_ingredient(
        name="Milk",
        purchasing_cost=Decimal("3.50"),
        unit_amount=1.0,
        unit_of_measure="liter",
        available=True,
    )

    with pytest.raises(DuplicateIngredientError) as exc_info:
        service.create_ingredient(
            name="Milk",
            purchasing_cost=Decimal("4.00"),
            unit_amount=2.0,
            unit_of_measure="liter",
            available=False,
        )

    assert "already in the repository" in str(exc_info.value)


def test_get_all_ingredients_returns_all_created_items(service):
    """Ensure all created ingredients are returned."""
    service.create_ingredient("Milk", Decimal("3.50"), 1.0, "liter", True)
    service.create_ingredient("Sugar", Decimal("1.00"), 2.0, "cup", False)

    all_ingredients = service.get_all_ingredients()

    assert len(all_ingredients) == 2
    assert [ingredient.name for ingredient in all_ingredients] == ["Milk", "Sugar"]


def test_get_available_ingredients_returns_only_available_items(service):
    """Ensure only available ingredients are returned."""
    service.create_ingredient("Milk", Decimal("3.50"), 1.0, "liter", True)
    service.create_ingredient("Sugar", Decimal("1.00"), 2.0, "cup", False)

    available_ingredients = service.get_available_ingredients()

    assert len(available_ingredients) == 1
    assert available_ingredients[0].name == "Milk"


def test_get_ingredient_by_name_returns_matching_ingredient(service):
    """Ensure ingredient lookup by name returns the correct item."""
    service.create_ingredient("Milk", Decimal("3.50"), 1.0, "liter", True)

    ingredient = service.get_ingredient_by_name("Milk")

    assert ingredient.name == "Milk"
    assert ingredient.available is True


def test_get_ingredient_by_name_raises_when_missing(service):
    """Ensure missing ingredients raise an error."""
    with pytest.raises(IngredientNotFound) as exc_info:
        service.get_ingredient_by_name("Milk")

    assert "No ingredient with name Milk" in str(exc_info.value)


def test_update_ingredient_updates_existing_ingredient(service):
    """Ensure updating an ingredient replaces its stored values."""
    service.create_ingredient("Milk", Decimal("3.50"), 1.0, "liter", True)

    service.update_ingredient("Milk", Decimal("4.00"), 2.0, "liter", False)

    updated_ingredient = service.get_ingredient_by_name("Milk")
    assert updated_ingredient.purchasing_cost == Decimal("4.00")
    assert updated_ingredient.unit_amount == 2.0
    assert updated_ingredient.available is False


def test_update_ingredient_raises_when_missing(service):
    """Ensure updating a missing ingredient raises an error."""
    with pytest.raises(IngredientNotFound) as exc_info:
        service.update_ingredient("Milk", Decimal("4.00"), 2.0, "liter", False)

    assert "No ingredient with name Milk" in str(exc_info.value)


def test_delete_ingredient_removes_the_ingredient(service):
    """Ensure deleting an ingredient removes it from the repository."""
    service.create_ingredient("Milk", Decimal("3.50"), 1.0, "liter", True)

    service.delete_ingredient("Milk")

    assert service.get_all_ingredients() == []


def test_delete_ingredient_raises_when_missing(service):
    """Ensure deleting a missing ingredient raises an error."""
    with pytest.raises(IngredientNotFound) as exc_info:
        service.delete_ingredient("Milk")

    assert "No ingredient with name Milk" in str(exc_info.value)