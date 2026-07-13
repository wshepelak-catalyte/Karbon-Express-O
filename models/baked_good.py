from decimal import Decimal
from dataclasses import dataclass, field

@dataclass
class BakedGood:
    """Domain model representing a baked good purchased from a vendor."""
    name: str
    vendor_name: str
    allergens: list[str]
    purchasing_cost: Decimal
    markup_percentage: Decimal
    
    # field(init=False) prevents this from being required in the constructor
    sale_price: Decimal = field(init=False)

    def __post_init__(self):
        """Automatically calculates the sale price when the object is created."""
        markup_amount = self.purchasing_cost * self.markup_percentage
        calculated_price = self.purchasing_cost + markup_amount
        
        # Rounds the calculated price to 2 decimal places for currency
        self.sale_price = calculated_price.quantize(Decimal('0.01'))