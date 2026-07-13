import pytest
from unittest.mock import Mock
from models.drink import Drink

@pytest.fixture
def mock_ingredient():
    return Mock()


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", 0.50, 3.0, 2.00),
        ("Latte", 0.80, 2.5, 2.80),
        ("Water", 0.00, 0.0, 0.00),
    ]
)
def test_drink_name_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.name == name


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", 0.50, 3.0, 2.00),
        ("Latte", 0.80, 2.5, 2.80),
        ("Water", 0.00, 0.0, 0.00),
    ]
)
def test_drink_ingredients_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.ingredients == ingredients


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", 0.50, 3.0, 2.00),
        ("Latte", 0.80, 2.5, 2.80),
        ("Water", 0.00, 0.0, 0.00),
    ]
)
def test_drink_cost_to_produce_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.cost_to_produce == cost_to_produce


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", 0.50, 3.0, 2.00),
        ("Latte", 0.80, 2.5, 2.80),
        ("Water", 0.00, 0.0, 0.00),
    ]
)
def test_drink_markup_percentage_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.markup_percentage == markup_percentage


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", 0.50, 3.0, 2.00),
        ("Latte", 0.80, 2.5, 2.80),
        ("Water", 0.00, 0.0, 0.00),
    ]
)
def test_drink_sale_price_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.sale_price == sale_price


def test_drink_equality_with_identical_attributes(mock_ingredient):
    drink_one = Drink("Espresso", [mock_ingredient], 0.50, 3.0, 2.00)
    drink_two = Drink("Espresso", [mock_ingredient], 0.50, 3.0, 2.00)
    assert drink_one == drink_two


def test_drink_inequality_with_different_names(mock_ingredient):
    drink_one = Drink("Espresso", [mock_ingredient], 0.50, 3.0, 2.00)
    drink_two = Drink("Short Espresso", [mock_ingredient], 0.50, 3.0, 2.00)
    assert drink_one != drink_two


@pytest.mark.parametrize(
    "attribute_name, mutated_value",
    [
        ("name", "Macchiato"),
        ("ingredients", []),
        ("cost_to_produce", 0.90),
        ("markup_percentage", 4.0),
        ("sale_price", 3.50),
    ]
)
def test_drink_mutability_after_initialization(mock_ingredient, attribute_name, mutated_value):
    drink = Drink("Latte", [mock_ingredient], 0.80, 2.5, 2.80)
    setattr(drink, attribute_name, mutated_value)
    assert getattr(drink, attribute_name) == mutated_value