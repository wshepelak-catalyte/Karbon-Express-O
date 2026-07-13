from dataclasses import dataclass
from decimal import Decimal

@dataclass
class BakedGood:
    """Domain model representing a baked good in the cafe inventory."""
    id: int
    name: str
    description: str
    price: Decimal
    cost_to_produce: Decimal
    quantity_in_stock: int
    is_vegan: bool = False
    is_gluten_free: bool = False
    
    def apply_discount(self, percentage: float) -> Decimal:
        """Applies a discount to the baked good."""
        discount_amount = self.price * Decimal(percentage)
        self.price -= discount_amount
        return self.price

    def is_in_stock(self) -> bool:
        """Checks if the item is currently available."""
        return self.quantity_in_stock > 0