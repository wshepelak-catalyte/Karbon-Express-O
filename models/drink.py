from dataclasses import dataclass
from decimal import Decimal
from models.ingredient import Ingredient

@dataclass
class Drink:
    """
        Represents an ingredient with cost and measurement information.
    """
    id: int
    name: str
    ingredients: list[Ingredient]
    cost_to_produce: Decimal
    markup_percentage: Decimal
    sale_price: Decimal

    def __post_init__(self):
        markup_amount = self.cost_to_produce * self.markup_percentage
        calculated_price = self.cost_to_produce + markup_amount        
        self.sale_price = calculated_price.quantize(Decimal('0.01'))

        if not isinstance(self.cost_to_produce, Decimal):
            self.cost_to_produce = Decimal(str(self.cost_to_produce))

        if not isinstance(self.sale_price, Decimal):
            self.sale_price = Decimal(str(self.sale_price))

        if self.cost_to_produce < Decimal("0"):
            raise ValueError("cost_to_produce cannot be negative")

        if self.markup_percentage < 0.0:
            raise ValueError("markup_percentage cannot be negative")

        if self.sale_price < Decimal("0"):
            raise ValueError("sale_price cannot be negative")