class BakedGood:
    """Domain model representing a baked good in the cafe inventory."""
    def __init__(self, item_id, name, description, price, cost_to_produce, quantity_in_stock, is_vegan=False, is_gluten_free=False):
        self.id = item_id
        self.name = name
        self.description = description

    