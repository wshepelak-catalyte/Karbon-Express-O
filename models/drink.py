from dataclasses import dataclass
from models.ingredient import Ingredient

@dataclass
class Drink:
    """
        Represents an ingredient with cost and measyrement information.
    """
    name: str
    ingredients: list[Ingredient]
    cost_to_produce: float
    markup_percentage: float
    sale_price: float