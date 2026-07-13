import pytest
from decimal import Decimal
from dataclasses import dataclass, field

# --- Your Model ---

@dataclass
class BakedGood:
    """Domain model representing a baked good purchased from a vendor."""
    name: str
    vendor_name: str
    allergens: list[str]
    purchasing_cost: Decimal
    markup_percentage: Decimal
    
    # field(init=False) tells the dataclass NOT to ask for this in the constructor
    sale_price: Decimal = field(init=False)

    def __post_init__(self):
        """Automatically calculates the sale price when the object is created."""
        markup_amount = self.purchasing_cost * self.markup_percentage
        calculated_price = self.purchasing_cost + markup_amount
        
        # The requirements ask for 2 decimal places for monetary values
        self.sale_price = calculated_price.quantize(Decimal('0.01'))


# --- Pytest Fixtures ---

@pytest.fixture
def cookie():
    """Fixture providing a fresh BakedGood instance for tests."""
    return BakedGood(
        name="Chocolate Chip Cookie",
        vendor_name="Sweet Treats Bakery",
        allergens=["wheat", "dairy", "eggs"],
        purchasing_cost=Decimal('1.50'),
        markup_percentage=Decimal('0.50') # 50% markup
    )

# --- Pytest Tests ---

def test_baked_good_initialization(cookie):
    """Tests that standard fields are set correctly."""
    assert cookie.name == "Chocolate Chip Cookie"
    assert cookie.vendor_name == "Sweet Treats Bakery"
    assert cookie.allergens == ["wheat", "dairy", "eggs"]
    assert cookie.purchasing_cost == Decimal('1.50')
    assert cookie.markup_percentage == Decimal('0.50')
    
def test_sale_price_calculation(cookie):
    """
    Tests that __post_init__ accurately calculates the sale_price 
    based on purchasing_cost and markup_percentage.
    $1.50 cost + 50% markup ($0.75) = $2.25
    """
    assert cookie.sale_price == Decimal('2.25')

def test_sale_price_rounding():
    """Tests that the calculated sale price cleanly rounds to 2 decimal places."""
    muffin = BakedGood(
        name="Blueberry Muffin",
        vendor_name="Morning Pastries",
        allergens=["wheat"],
        purchasing_cost=Decimal('1.25'),
        markup_percentage=Decimal('0.333') # A messy markup percentage
    )
    # 1.25 * 0.333 = 0.41625
    # 1.25 + 0.41625 = 1.66625 -> Should round to 1.67
    assert muffin.sale_price == Decimal('1.67')