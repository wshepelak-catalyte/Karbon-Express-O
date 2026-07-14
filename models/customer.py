"""
Customer model for representing customers and their purchases.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.purchase import Purchase

@dataclass
class Customer:
    """
    Represents a Customer with name, email, phone, username, spending, and purchase history.

    Attributes:
        name (str): The name of the customer.
        email (str): The email of the customer.
        phone (str): The customer's phone number.
        username (str): The customer's username.
        lifetime_spend (Decimal | float): The amount spent by the customer.
        purchases (list[Purchase]): The list of purchases made by the customer.
    """
    id: int
    name: str
    email: str
    phone: str
    username: str
    lifetime_spend: float | Decimal
    purchases: list["Purchase"] = field(default_factory=list)

    def __post_init__(self):
        """
            Cast lifetime spend input as Decimal object on initialization
        """
        if not isinstance(self.lifetime_spend, Decimal):
            self.lifetime_spend = Decimal(str(self.lifetime_spend))

    def add_purchase(self, purchase: "Purchase") -> None:
        """Add a purchase to the customer's history and update lifetime spend."""
        self.purchases.append(purchase)
        if not isinstance(purchase.total_cost, Decimal):
            purchase.total_cost = Decimal(str(purchase.total_cost))
        self.lifetime_spend += Decimal(str(purchase.total_cost))

    def __str__(self)->str:
        """
        String representation for a Customer
        """
        result_string = "Customer\n"
        result_string += f"   Id: {str(self.id)}\n"
        result_string += f"   Name: {self.name}\n"
        result_string += f"   Email: {self.email}\n"
        result_string += f"   Phone: {self.phone}\n"
        result_string += f"   Username: {self.username}\n"
        result_string += f"   Lifetime Spend: ${str(self.lifetime_spend)}\n"
        result_string += f"   Purchases: {len(self.purchases)}"
        return result_string

        