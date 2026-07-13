from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from models.customer import Customer

@dataclass
class Purchase:
    """
        Represents a purchase with cost and measurement information.
    """
    id: int
    timestamp: datetime
    items: list[any]
    total_cost: Decimal
    customer: Customer

    def __post_init__(self):
        self.timestamp = datetime.now(timezone.utc)