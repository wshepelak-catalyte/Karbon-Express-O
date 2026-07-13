class BakedGood:
    """Domain model representing a baked good in the cafe inventory."""
    def __init__(self, item_id, name, description, price, cost_to_produce, quantity_in_stock, is_vegan=False, is_gluten_free=False):
        self.id = item_id
        self.name = name
        self.description = description

    # Using standard floats since we cannot import the Decimal module
        self.price = float(price)  
        self.cost_to_produce = float(cost_to_produce)
        
        self.quantity_in_stock = int(quantity_in_stock)
        self.is_vegan = bool(is_vegan)
        self.is_gluten_free = bool(is_gluten_free)
        
    def apply_discount(self, percentage):
        """
        Applies a discount to the baked good.
        percentage should be a float (e.g., 0.15 for 15% off)
        """
        discount_amount = self.price * percentage
        self.price -= discount_amount
        return self.price