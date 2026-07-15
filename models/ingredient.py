"""
Ingredient model for representing purchasable items and their measurement units.
"""

from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Ingredient:
    """
    Represents an ingredient with cost and measurement information.

    Attributes:
        name (str): The name of the ingredient.
        purchasing_cost (Decimal | float): The cost to purchase the ingredient. Must be non-negative.
        unit_amount (float): The quantity of the ingredient. Must be greater than zero.
        unit_of_measure (str): The unit used to measure the ingredient (e.g., grams, liters).
    """
    id: int
    name: str
    purchasing_cost: Decimal | float
    unit_amount: float
    unit_of_measure: str
    available : bool

    def __post_init__(self):
        """
        Validate fields after initialization.

        Raises:
            ValueError: If purchasing_cost is negative or unit_amount is not greater than zero.
        """
        if not isinstance(self.purchasing_cost, Decimal):
            self.purchasing_cost = Decimal(str(self.purchasing_cost))

        if self.purchasing_cost < Decimal("0"):
            raise ValueError("purchasing_cost cnnot be negative")
        
        if self.unit_amount <= 0:
            raise ValueError("unit_amount must be greater than zero")
        
    def __str__(self)->str:
        """
        String representation for an Ingredient object
        """

        result_string = ""
        result_string += f"Ingredient\n"
        result_string += f"   Id: {str(self.id)}\n"
        result_string += f"   Name: {self.name}\n"
        result_string += f"   Purchasing Cost: {str(self.purchasing_cost)}\n"
        result_string += f"   Unit Amount: {str(self.unit_amount)}\n"
        result_string += f"   Unit of Measure: {self.unit_of_measure}\n"
        result_string += f"   Available: {"True" if self.available else "False"}"

        return result_string