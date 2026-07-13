"""
Tests for the IngredientRepository class.
"""

import pytest
from decimal import Decimal
from models.ingredient import Ingredient
from repositories.ingredient_repository import IngredientRepository

def test_add_and_get_all():
    """Ensure ingredients are added and retrieved correctly."""
    repo = IngredientRepository()
    milk = Ingredient("Milk", Decimal("3.50"), 1.0, "liter")
    salt = Ingredient("Salt", Decimal("0.25"), 3.5, "gram")

    repo.add(milk)
    repo.add(salt)

    all_items = repo.get_all()

    assert len(all_items) == 2
    assert all_items[0].name == "Milk"
    assert all_items[1].name == "Salt"

def test_get_by_name_found():
    """Ensure get_by_name retrns the correct ingredient."""
    repo = IngredientRepository()
    ingredient = Ingredient("Sugar", Decimal("1.00"), 2.0, "cup")
    repo.add(ingredient)

    result = repo.get_by_name("Sugar")

    assert result is not None
    assert result.name == "Sugar"

def test_get_by_name_not_found():
    """Ensure get_by_name returns None wen ingredient does not exist."""
    repo = IngredientRepository()
    result = repo.get_by_name("NotReal")

    assert result is None

def test_update_success():
    """Ensure update replaces the correct ingredient."""
    repo = IngredientRepository()
    old = Ingredient("Milk", Decimal("3.50"), 1.0, "liter")
    new = Ingredient("Milk", Decimal("4.00"), 2.0, "liter")

    repo.add(old)
    updated = repo.update("Milk", new)

    assert updated is not None
    assert updated.purchasing_cost == Decimal("4.00")
    assert updated.unit_amount == 2.0

def test_update_not_found():
    """Ensure update returns None when ingredient does not exist."""
    repo = IngredientRepository()
    new = Ingredient("Milk", Decimal("4.00"), 2.0, "liter")

    result = repo.update("NotReal", new)

    assert result is None

def test_delete_success():
    """Ensure delete removes the ingredient and returns True."""
    repo = IngredientRepository()
    ingredient = Ingredient("Salt", Decimal("0.25"), 3.5, "gram")
    repo.add(ingredient)

    deleted = repo.delete("Salt")

    assert deleted is True
    assert repo.get_by_name("Salt") is None

def test_delete_not_found():
    """Ensure delete returns False when ingredient does not exist."""
    repo = IngredientRepository()

    deleted = repo.delete("NotReal")

    assert deleted is False