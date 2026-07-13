from decimal import Decimal

class BakedGood:
    """Domain model representing a baked good in the cafe inventory."""
    
    def __init__(self, item_id: int, name: str, description: str, price, cost_to_produce, quantity_in_stock: int, is_vegan: bool = False, is_gluten_free: bool = False):
        self.id = item_id
        self.name = name
        self.description = description
        
        # Using Decimal for precise monetary representation
        self.price: Decimal = Decimal(str(price))  
        self.cost_to_produce: Decimal = Decimal(str(cost_to_produce))
        
        self.quantity_in_stock = int(quantity_in_stock)
        self.is_vegan = bool(is_vegan)
        self.is_gluten_free = bool(is_gluten_free)
        
    def apply_discount(self, percentage) -> Decimal:
        """
        Applies a discount to the baked good.
        percentage can be a float or string (e.g., '0.15' or 0.15 for 15% off)
        """
        discount_amount = self.price * Decimal(str(percentage))
        self.price -= discount_amount
        return self.price

    def is_in_stock(self) -> bool:
        """Checks if the item is currently available."""
        return self.quantity_in_stock > 0
        
    def __str__(self) -> str:
        """Returns a readable string representation of the object."""
        return f"{self.name} - ${self.price:.2f} ({self.quantity_in_stock} in stock)"