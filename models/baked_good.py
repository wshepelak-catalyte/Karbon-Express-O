from decimal import Decimal


class BakedGood:
    """Domain model representing a baked good purchased from a vendor."""

    def __init__(
        self,
        id: int,
        name: str,
        vendor_name: str,
        allergens: list[str],
        purchasing_cost: Decimal | float,
        markup_percentage: Decimal | float,
        available: bool = True,
    ):
        self.id = id
        self.name = name
        self.vendor_name = vendor_name
        self.allergens = allergens
        self.purchasing_cost = Decimal(str(purchasing_cost))
        self.markup_percentage = Decimal(str(markup_percentage))
        self.available = bool(available)
        self.sale_price = self._calculate_sale_price()

    def _calculate_sale_price(self) -> Decimal:
        markup_amount = self.purchasing_cost * self.markup_percentage
        calculated_price = self.purchasing_cost + markup_amount
        return calculated_price.quantize(Decimal("0.01"))

    def __str__(self) -> str:
        return f"{self.name} - ${self.sale_price:.2f}"
