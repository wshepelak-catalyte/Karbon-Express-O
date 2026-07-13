from decimal import Decimal
from unittest.mock import Mock
import pytest
from models.drink import Drink


@pytest.fixture
def mock_ingredient():
    return Mock()


@pytest.fixture
def valid_drink():
    mock_ingredient = Mock()
    return Drink(
        name="Latte",
        ingredients=[mock_ingredient],
        cost_to_produce=Decimal("0.80"),
        markup_percentage=Decimal("2.5"),
        sale_price=Decimal("2.80")
    )


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", Decimal("0.50"), Decimal("3.0"), Decimal("2.00")),
        ("Latte", Decimal("0.80"), Decimal("2.5"), Decimal("2.80")),
        ("Water", Decimal("0.00"), Decimal("0.0"), Decimal("0.00")),
    ]
)
def test_drink_name_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.name == name


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", Decimal("0.50"), Decimal("3.0"), Decimal("2.00")),
        ("Latte", Decimal("0.80"), Decimal("2.5"), Decimal("2.80")),
        ("Water", Decimal("0.00"), Decimal("0.0"), Decimal("0.00")),
    ]
)
def test_drink_ingredients_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.ingredients == ingredients


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", Decimal("0.50"), Decimal("3.0"), Decimal("2.00")),
        ("Latte", Decimal("0.80"), Decimal("2.5"), Decimal("2.80")),
        ("Water", Decimal("0.00"), Decimal("0.0"), Decimal("0.00")),
    ]
)
def test_drink_cost_to_produce_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.cost_to_produce == cost_to_produce


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", Decimal("0.50"), Decimal("3.0"), Decimal("2.00")),
        ("Latte", Decimal("0.80"), Decimal("2.5"), Decimal("2.80")),
        ("Water", Decimal("0.00"), Decimal("0.0"), Decimal("0.00")),
    ]
)
def test_drink_markup_percentage_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.markup_percentage == markup_percentage


@pytest.mark.parametrize(
    "name, cost_to_produce, markup_percentage, sale_price",
    [
        ("Espresso", Decimal("0.50"), Decimal("3.0"), Decimal("2.00")),
        ("Latte", Decimal("0.80"), Decimal("2.5"), Decimal("2.80")),
        ("Water", Decimal("0.00"), Decimal("0.0"), Decimal("0.00")),
    ]
)
def test_drink_sale_price_initialization(mock_ingredient, name, cost_to_produce, markup_percentage, sale_price):
    ingredients = [mock_ingredient] if name != "Water" else []
    drink = Drink(name, ingredients, cost_to_produce, markup_percentage, sale_price)
    assert drink.sale_price == sale_price


def test_drink_equality_with_identical_attributes(mock_ingredient):
    drink_one = Drink("Espresso", [mock_ingredient], Decimal("0.50"), Decimal("3.0"), Decimal("2.00"))
    drink_two = Drink("Espresso", [mock_ingredient], Decimal("0.50"), Decimal("3.0"), Decimal("2.00"))
    assert drink_one == drink_two


def test_drink_inequality_with_different_names(mock_ingredient):
    drink_one = Drink("Espresso", [mock_ingredient], Decimal("0.50"), Decimal("3.0"), Decimal("2.00"))
    drink_two = Drink("Short Espresso", [mock_ingredient], Decimal("0.50"), Decimal("3.0"), Decimal("2.00"))
    assert drink_one != drink_two


@pytest.mark.parametrize(
    "attribute_name, mutated_value",
    [
        ("name", "Macchiato"),
        ("ingredients", []),
        ("cost_to_produce", Decimal("0.90")),
        ("markup_percentage", Decimal("4.0")),
        ("sale_price", Decimal("3.50")),
    ]
)
def test_drink_mutability_after_initialization(mock_ingredient, attribute_name, mutated_value):
    drink = Drink("Latte", [mock_ingredient], Decimal("0.80"), Decimal("2.5"), Decimal("2.80"))
    setattr(drink, attribute_name, mutated_value)
    assert getattr(drink, attribute_name) == mutated_value


def test_drink_name_attribute_type_is_string(valid_drink):
    assert isinstance(valid_drink.name, str)


def test_drink_ingredients_attribute_type_is_list(valid_drink):
    assert isinstance(valid_drink.ingredients, list)


def test_drink_cost_to_produce_attribute_type_is_decimal(valid_drink):
    assert isinstance(valid_drink.cost_to_produce, Decimal)


def test_drink_markup_percentage_attribute_type_is_decimal(valid_drink):
    assert isinstance(valid_drink.markup_percentage, Decimal)


def test_drink_sale_price_attribute_type_is_decimal(valid_drink):
    assert isinstance(valid_drink.sale_price, Decimal)