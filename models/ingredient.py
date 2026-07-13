"""
Ingredient model for representing purchaseable items and their measurement units.
"""

# modles/ingredient.py

from dataclasses import dataclass

@dataclass
class Ingredient:
    """
    Represents an ingredient with cost and measyrement information.
    """
    name: str
    purchasing_cost: float
    unit_amount: float
    unit_of_measure: str
