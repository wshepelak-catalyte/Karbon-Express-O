# ...existing code...
from decimal import Decimal
from dataclasses import dataclass, field
from typing import List

@dataclass
class BakedGood:
    """Domain model representing a baked good purchased from a vendor."""
    name: str
    vendor_name: str
    allergens: List[str]
    purchasing_cost: Decimal
    markup_percentage: Decimal

    # field(init=False) prevents this from being required in the constructor
    sale_price: Decimal = field(init=False)

    def __post_init__(self):
        """Normalize inputs, validate, and calculate the sale price."""
        def _to_decimal(v):
            if isinstance(v, Decimal):
                return v
            if isinstance(v, float):
                return Decimal(str(v))
            return Decimal(v)

        self.purchasing_cost = _to_decimal(self.purchasing_cost)
        self.markup_percentage = _to_decimal(self.markup_percentage)

        if self.purchasing_cost < 0:
            raise ValueError("purchasing_cost must be non-negative")
        if self.markup_percentage < 0:
            raise ValueError("markup_percentage must be non-negative")

        # Accept either a fractional markup (0.20) or a percent (20)
        if self.markup_percentage > 1 and self.markup_percentage <= 100:
            self.markup_percentage = (self.markup_percentage / Decimal(100))

        markup_amount = (self.purchasing_cost * self.markup_percentage).quantize(Decimal('0.01'))
        self.sale_price = (self.purchasing_cost + markup_amount).quantize(Decimal('0.01'))
# ...existing code...
