from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class BakedGood:
    """Domain model representing a baked good purchased from a vendor."""

    id: int
    name: str
    vendor_name: str
    allergens: list[str]
    purchasing_cost: Decimal | float
    markup_percentage: Decimal | float
    sale_price: Decimal = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.purchasing_cost, Decimal):
            self.purchasing_cost = Decimal(str(self.purchasing_cost))

        if not isinstance(self.markup_percentage, Decimal):
            self.markup_percentage = Decimal(str(self.markup_percentage))

        if self.purchasing_cost < Decimal("0"):
            raise ValueError("purchasing_cost cannot be negative")

        if self.markup_percentage < Decimal("0"):
            raise ValueError("markup_percentage cannot be negative")

        markup_amount = self.purchasing_cost * self.markup_percentage
        calculated_price = self.purchasing_cost + markup_amount
        self.sale_price = calculated_price.quantize(Decimal("0.01"))

    def __str__(self) -> str:
        return f"{self.name} - ${self.sale_price:.2f}"
