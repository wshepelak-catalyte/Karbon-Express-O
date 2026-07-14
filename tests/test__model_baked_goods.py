import pytest
from decimal import Decimal

from models.baked_good import BakedGood


@pytest.fixture
def cookie():
    """Fixture providing a fresh BakedGood instance for tests."""
    return BakedGood(
        id=1,
        name="Chocolate Chip Cookie",
        vendor_name="Sweet Treats Bakery",
        allergens=["wheat", "dairy", "eggs"],
        purchasing_cost=Decimal("1.50"),
        markup_percentage=Decimal("0.50"),
    )


def test_baked_good_initialization(cookie):
    """Tests that standard fields are set correctly."""
    assert cookie.id == 1
    assert cookie.name == "Chocolate Chip Cookie"
    assert cookie.vendor_name == "Sweet Treats Bakery"
    assert cookie.allergens == ["wheat", "dairy", "eggs"]
    assert cookie.purchasing_cost == Decimal("1.50")
    assert cookie.markup_percentage == Decimal("0.50")


def test_sale_price_calculation(cookie):
    """
    Tests that the sale_price is calculated based on purchasing_cost and markup_percentage.
    $1.50 cost + 50% markup ($0.75) = $2.25.
    """
    assert cookie.sale_price == Decimal("2.25")


def test_sale_price_rounding():
    """Tests that the calculated sale price cleanly rounds to 2 decimal places."""
    muffin = BakedGood(
        id=2,
        name="Blueberry Muffin",
        vendor_name="Morning Pastries",
        allergens=["wheat"],
        purchasing_cost=Decimal("1.25"),
        markup_percentage=Decimal("0.333"),
    )
    assert muffin.sale_price == Decimal("1.67")