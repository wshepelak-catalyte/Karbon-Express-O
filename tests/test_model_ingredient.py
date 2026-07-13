"""
Tests for the Ingredent model.
"""

import pytest
from models.ingredient import Ingredient
from decimal import Decimal


@pytest.mark.parametrize(
        "ingredient, expected_name, expected_cost, expected_amount, expected_measure",
        [
            (
                Ingredient(
                    name="Milk",
                    purchasing_cost=3.50,
                    unit_amount=1.0,
                    unit_of_measure="liter"
                ),
                "Milk",
                Decimal("3.50"),
                1.0,
                "liter"
            ),
            (
                Ingredient(
                    name="Salt",
                    purchasing_cost=0.25,
                    unit_amount=3.5,
                    unit_of_measure="gram"
                ),
                "Salt",
                Decimal("0.25"),
                3.5,
                "gram"
            )

        ]
)
def test_ingredient_initialization(ingredient, expected_name, expected_cost, expected_amount, expected_measure):
    """Ensure Ingredient initializes with correct attribute values."""
    assert ingredient.name == expected_name
    assert ingredient.purchasing_cost == expected_cost
    assert ingredient.unit_amount == expected_amount
    assert ingredient.unit_of_measure == expected_measure

@pytest.mark.parametrize(
        "ingredient",
        [
            Ingredient(
                name="Milk",
                purchasing_cost=3.50,
                unit_amount=1.0,
                unit_of_measure="liter"
            ),
            Ingredient(
                name="Salt",
                purchasing_cost=0.25,
                unit_amount=3.5,
                unit_of_measure="gram"
            ),
        ]
)
def test_ingredient_types(ingredient):
    """Verify Ingredient fields have correct types."""
    assert isinstance(ingredient.name, str)
    assert isinstance(ingredient.purchasing_cost, Decimal)
    assert isinstance(ingredient.unit_amount, float)
    assert isinstance(ingredient.unit_of_measure, str)

def test_ingredient_invalid_cost():
    """Ensure negative purchasing_cost is logically invalid."""
    with pytest.raises(ValueError):
        Ingredient("Coffee Beans", -10.0, 1.0, "kg")