"""
Customer model for representing customers and their purchases.
"""

import re
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Customer:
    """
    Represents a Customer with name email, and spending information

    Attributes:
        name (str): The name of the customer.
        email (str): The email of the customer.
        lifetime_spent (Decimal): The life amount spent by the customer.
    """
    name: str
    email: str
    lifetime_spend: float | Decimal

    def __post_init__(self):
        """
            Cast lifetime spend input as Decimal object on initialization
        """
        if not isinstance(self.lifetime_spend, Decimal):
            self.lifetime_spend = Decimal(str(self.lifetime_spend))

    def __str__(self):
        """
        String representation for a Customer
        """
        result_string = "Customer\n"
        result_string += f"   Name: {self.name}\n"
        result_string += f"   Email: {self.email}\n"
        result_string += f"   Lifetime Spend: ${str(self.lifetime_spend)}"

        return result_string

        