from dataclasses import dataclass
import decimal
from models.ingredient import Ingredient

@dataclass
class Drink:
    """
        Represents an ingredient with cost and measyrement information.
    """
    name: str
    ingredients: list[Ingredient]
    cost_to_produce: decimal
    markup_percentage: decimal
    sale_price: decimal