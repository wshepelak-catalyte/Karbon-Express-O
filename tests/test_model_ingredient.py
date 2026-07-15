"""
Tests for the Ingredient model.
"""

import pytest
from decimal import Decimal
from models.ingredient import Ingredient


@pytest.mark.parametrize(
    "ingredient, expected_id, expected_name, expected_cost, expected_amount, expected_measure, expected_available",
    [
        (
            Ingredient(
                id=1,
                name="Milk",
                purchasing_cost=3.50,
                unit_amount=1.0,
                unit_of_measure="liter",
                available=True,
            ),
            1,
            "Milk",
            Decimal("3.50"),
            1.0,
            "liter",
            True,
        ),
        (
            Ingredient(
                id=2,
                name="Salt",
                purchasing_cost=0.25,
                unit_amount=3.5,
                unit_of_measure="gram",
                available=False,
            ),
            2,
            "Salt",
            Decimal("0.25"),
            3.5,
            "gram",
            False,
        ),
    ],
)
def test_ingredient_initialization(
    ingredient,
    expected_id,
    expected_name,
    expected_cost,
    expected_amount,
    expected_measure,
    expected_available,
):
    """Ensure Ingredient initializes with correct attribute values."""
    assert ingredient.id == expected_id
    assert ingredient.name == expected_name
    assert ingredient.purchasing_cost == expected_cost
    assert ingredient.unit_amount == expected_amount
    assert ingredient.unit_of_measure == expected_measure
    assert ingredient.available is expected_available


@pytest.mark.parametrize(
    "ingredient",
    [
        Ingredient(
            id=1,
            name="Milk",
            purchasing_cost=3.50,
            unit_amount=1.0,
            unit_of_measure="liter",
            available=True,
        ),
        Ingredient(
            id=2,
            name="Salt",
            purchasing_cost=0.25,
            unit_amount=3.5,
            unit_of_measure="gram",
            available=False,
        ),
    ],
)
def test_ingredient_types(ingredient):
    """Verify Ingredient fields have correct types."""
    assert isinstance(ingredient.id, int)
    assert isinstance(ingredient.name, str)
    assert isinstance(ingredient.purchasing_cost, Decimal)
    assert isinstance(ingredient.unit_amount, float)
    assert isinstance(ingredient.unit_of_measure, str)
    assert isinstance(ingredient.available, bool)


def test_ingredient_invalid_cost():
    """Ensure negative purchasing_cost is logically invalid."""
    with pytest.raises(ValueError):
        Ingredient(
            id=1,
            name="Coffee Beans",
            purchasing_cost=-10.0,
            unit_amount=1.0,
            unit_of_measure="kg",
            available=True,
        )


def test_ingredient_string_cast():
    """Verify Ingredient string cast is correctly formatted."""
    test_ingredient = Ingredient(
        id=1,
        name="Milk",
        purchasing_cost=Decimal("3.50"),
        unit_amount=1.0,
        unit_of_measure="liter",
        available=True,
    )

    assert str(test_ingredient) == (
        "Ingredient\n"
        "   Id: 1\n"
        "   Name: Milk\n"
        "   Purchasing Cost: 3.50\n"
        "   Unit Amount: 1.0\n"
        "   Unit of Measure: liter\n"
        "   Available: True"
    )