from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from numbers import Number
from typing import Any
from models.customer import Customer


@dataclass
class Purchase:
    """
        Represents a purchase with cost and measurement information.
    """
    id: Number
    timestamp: datetime
    items: list[Any]
    total_cost: Decimal
    customer: Customer

    def __post_init__(self):
        self.timestamp = datetime.now(timezone.utc)