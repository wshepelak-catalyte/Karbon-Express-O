from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from numbers import Number
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from models.customer import Customer


@dataclass
class Purchase:
    """
        Represents a purchase with cost and measurement information.
    """
    id: int
    timestamp: datetime
    items: list[Any]
    total_cost: Decimal
    customer: Customer

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)