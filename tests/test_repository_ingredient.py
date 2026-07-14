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
    milk = Ingredient(id=1, name="Milk", purchasing_cost=Decimal("3.50"), unit_amount=1.0, unit_of_measure="liter")
    salt = Ingredient(id=2, name="Salt", purchasing_cost=Decimal("0.25"), unit_amount=3.5, unit_of_measure="gram")

    repo.add(milk)
    repo.add(salt)

    all_items = repo.get_all()

    assert len(all_items) == 2
    assert all_items[0].name == "Milk"
    assert all_items[1].name == "Salt"

def test_get_by_name_found():
    """Ensure get_by_name retrns the correct ingredient."""
    repo = IngredientRepository()
    ingredient = Ingredient(id=1, name="Sugar", purchasing_cost=Decimal("1.00"), unit_amount=2.0, unit_of_measure="cup")
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
    old = Ingredient(id=1, name="Milk", purchasing_cost=Decimal("3.50"), unit_amount=1.0, unit_of_measure="liter")
    new = Ingredient(id=1, name="Milk", purchasing_cost=Decimal("4.00"), unit_amount=2.0, unit_of_measure="liter")

    repo.add(old)
    updated = repo.update("Milk", new)

    assert updated is not None
    assert updated.purchasing_cost == Decimal("4.00")
    assert updated.unit_amount == 2.0

def test_update_not_found():
    """Ensure update returns None when ingredient does not exist."""
    repo = IngredientRepository()
    new = Ingredient(id=1, name="Milk", purchasing_cost=Decimal("4.00"), unit_amount=2.0, unit_of_measure="liter")

    result = repo.update("NotReal", new)

    assert result is None

def test_delete_success():
    """Ensure delete removes the ingredient and returns True."""
    repo = IngredientRepository()
    ingredient = Ingredient(id=1, name="Salt", purchasing_cost=Decimal("0.25"), unit_amount=3.5, unit_of_measure="gram")
    repo.add(ingredient)

    deleted = repo.delete("Salt")

    assert deleted is True
    assert repo.get_by_name("Salt") is None

def test_delete_not_found():
    """Ensure delete returns False when ingredient does not exist."""
    repo = IngredientRepository()

    deleted = repo.delete("NotReal")

    assert deleted is False